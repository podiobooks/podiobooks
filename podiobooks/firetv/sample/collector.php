<?php
// Podiobooks Channel Server
// =============================================================================
//
// * Author: [Craig Davis](craig@there4development.com)
// * Since: 9/21/2015
//
// -----------------------------------------------------------------------------
//

require_once __DIR__ . '/../vendor/autoload.php';

use PicoFeed\Reader\Reader;
use PicoFeed\Config\Config;


$reader = new Reader;

// Fetch all titles
$resource = $reader->download('http://podiobooks.com/rss/feeds/titles/');
$parser = $reader->getParser(
    $resource->getUrl(),
    $resource->getContent(),
    $resource->getEncoding()
);
$feed = $parser->execute();

$titleUrls = [];
foreach ($feed->getItems() as $item) {
    $titleUrls[] = $item->getUrl();
}

//$titleUrls = array_slice($titleUrls, 0, 100);

$folders = [];
$media   = [];

$folderIdCount = 1;

$folders['root'] = [
    'id'          => $folderIdCount++,
    'title'       => 'root',
    'imgURL'      => '',
    'description' => '',
    'contents'    => []
];

// Fetch all the details for each
foreach ($titleUrls as $url) {
    print " Parsing $url\n";
    flush();

    $resource = $reader->download($url);
    $parser = $reader->getParser(
        $resource->getUrl(),
        $resource->getContent(),
        $resource->getEncoding()
    );
    $title = $parser->execute();

    // Categories are non-standard and we must parse for them ourselves
    $doc = new DOMDocument();
    $doc->preserveWhiteSpace = false;
    $doc->loadXML($resource->getContent());

    $xpath = new DOMXpath($doc);
    $xpath->registerNamespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd');
    $channel = $doc->getElementsByTagName('channel')->item(0);

    $category = $xpath->query('category', $channel)->item(0)->nodeValue;
    $image = $xpath->query('itunes:image', $channel)->item(0)->getAttribute('href');

    // If the category channel doesn't exist, create it as a top level folder
    // Potential bug here if a book name matches a category name
    if (!isset($folders[$category])) {
        $topLevelId = $folderIdCount++;
        $folders[$category] = [
            'id'          => $topLevelId,
            'title'       => $category,
            'imgURL'      => '',
            'description' => $category . ' Podiobooks',
            'contents'    => []
        ];
        // Add this to the root folder
        $folders['root']['contents'][] = ['type' => 'folder', 'id' => $topLevelId];
    }

    // Add this entry as a folder
    $titleId = $folderIdCount++;
    $folders[$title->getTitle()] = [
        'id'          => $titleId,
        'title'       => $title->getTitle(),
        'imgURL'      => $image,
        'description' => @iconv('UTF-8//IGNORE', 'UTF-8', $title->getDescription()),
        'contents'    => [ /* episode list goes here */]
    ];

    // Add this record as a sub category to the parent category
    $folders[$category]['contents'][] = ['type' => 'folder', 'id' => $titleId];

    // Process to fetch each episode
    foreach ($title->getItems() as $episode) {
        print ".";
        flush();
        $mediaId = uniqid();
        $folders[$title->getTitle()]['contents'][] = [
            'type' => 'media',
            'id'   => $mediaId
        ];
        $media[] = [
            'id'          => $mediaId,
            'title'       => $episode->getTitle(),
            'pubDate'     => $episode->date->format(DATE_RFC822),
            'thumbURL'    => $image,
            'imgURL'      => $image,
            'videoURL'    => $episode->getEnclosureUrl(),
            'type'        => 'audio',
            'categories'  => [$category],
            'description' => @iconv('UTF-8//IGNORE', 'UTF-8', $episode->getTag('itunes:summary')[0])
        ];
    }
    print "\n";
}

$json = [
    'folders' => array_values($folders),
    'media' => $media
];

$output = json_encode($json, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);

print "length: " . strlen($output) . "\n";
print json_last_error_msg();

file_put_contents('channel-data.json', $output);
print "Complete\n";

/* End of file collector.php */
