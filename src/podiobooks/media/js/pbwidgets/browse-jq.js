function populateContributorBrowseLists() {
	console.log('bob');
	$('#pb-header-menubar').append("<div id='pb-browse-lists'></div>");
	$('#pb-browse-lists').load('/contributor');
}
