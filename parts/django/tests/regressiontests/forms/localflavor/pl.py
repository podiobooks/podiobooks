# -*- coding: utf-8 -*-
# Tests for the contrib/localflavor/ PL form fields.

tests = r"""
# PLProvinceSelect ##########################################################

>>> from django.contrib.localflavor.pl.forms import PLProvinceSelect
>>> f = PLProvinceSelect()
>>> f.render('voivodeships','pomerania')
u'<select name="voivodeships">\n<option value="lower_silesia">Lower Silesia</option>\n<option value="kuyavia-pomerania">Kuyavia-Pomerania</option>\n<option value="lublin">Lublin</option>\n<option value="lubusz">Lubusz</option>\n<option value="lodz">Lodz</option>\n<option value="lesser_poland">Lesser Poland</option>\n<option value="masovia">Masovia</option>\n<option value="opole">Opole</option>\n<option value="subcarpatia">Subcarpatia</option>\n<option value="podlasie">Podlasie</option>\n<option value="pomerania" selected="selected">Pomerania</option>\n<option value="silesia">Silesia</option>\n<option value="swietokrzyskie">Swietokrzyskie</option>\n<option value="warmia-masuria">Warmia-Masuria</option>\n<option value="greater_poland">Greater Poland</option>\n<option value="west_pomerania">West Pomerania</option>\n</select>'

# PLCountySelect ##########################################################

>>> from django.contrib.localflavor.pl.forms import PLCountySelect
>>> f = PLCountySelect()
>>> f.render('administrativeunit','katowice')
u'<select name="administrativeunit">\n<option value="wroclaw">Wroc\u0142aw</option>\n<option value="jeleniagora">Jelenia G\xf3ra</option>\n<option value="legnica">Legnica</option>\n<option value="boleslawiecki">boles\u0142awiecki</option>\n<option value="dzierzoniowski">dzier\u017coniowski</option>\n<option value="glogowski">g\u0142ogowski</option>\n<option value="gorowski">g\xf3rowski</option>\n<option value="jaworski">jaworski</option>\n<option value="jeleniogorski">jeleniog\xf3rski</option>\n<option value="kamiennogorski">kamiennog\xf3rski</option>\n<option value="klodzki">k\u0142odzki</option>\n<option value="legnicki">legnicki</option>\n<option value="lubanski">luba\u0144ski</option>\n<option value="lubinski">lubi\u0144ski</option>\n<option value="lwowecki">lw\xf3wecki</option>\n<option value="milicki">milicki</option>\n<option value="olesnicki">ole\u015bnicki</option>\n<option value="olawski">o\u0142awski</option>\n<option value="polkowicki">polkowicki</option>\n<option value="strzelinski">strzeli\u0144ski</option>\n<option value="sredzki">\u015bredzki</option>\n<option value="swidnicki">\u015bwidnicki</option>\n<option value="trzebnicki">trzebnicki</option>\n<option value="walbrzyski">wa\u0142brzyski</option>\n<option value="wolowski">wo\u0142owski</option>\n<option value="wroclawski">wroc\u0142awski</option>\n<option value="zabkowicki">z\u0105bkowicki</option>\n<option value="zgorzelecki">zgorzelecki</option>\n<option value="zlotoryjski">z\u0142otoryjski</option>\n<option value="bydgoszcz">Bydgoszcz</option>\n<option value="torun">Toru\u0144</option>\n<option value="wloclawek">W\u0142oc\u0142awek</option>\n<option value="grudziadz">Grudzi\u0105dz</option>\n<option value="aleksandrowski">aleksandrowski</option>\n<option value="brodnicki">brodnicki</option>\n<option value="bydgoski">bydgoski</option>\n<option value="chelminski">che\u0142mi\u0144ski</option>\n<option value="golubsko-dobrzynski">golubsko-dobrzy\u0144ski</option>\n<option value="grudziadzki">grudzi\u0105dzki</option>\n<option value="inowroclawski">inowroc\u0142awski</option>\n<option value="lipnowski">lipnowski</option>\n<option value="mogilenski">mogile\u0144ski</option>\n<option value="nakielski">nakielski</option>\n<option value="radziejowski">radziejowski</option>\n<option value="rypinski">rypi\u0144ski</option>\n<option value="sepolenski">s\u0119pole\u0144ski</option>\n<option value="swiecki">\u015bwiecki</option>\n<option value="torunski">toru\u0144ski</option>\n<option value="tucholski">tucholski</option>\n<option value="wabrzeski">w\u0105brzeski</option>\n<option value="wloclawski">wroc\u0142awski</option>\n<option value="zninski">\u017ani\u0144ski</option>\n<option value="lublin">Lublin</option>\n<option value="biala-podlaska">Bia\u0142a Podlaska</option>\n<option value="chelm">Che\u0142m</option>\n<option value="zamosc">Zamo\u015b\u0107</option>\n<option value="bialski">bialski</option>\n<option value="bilgorajski">bi\u0142gorajski</option>\n<option value="chelmski">che\u0142mski</option>\n<option value="hrubieszowski">hrubieszowski</option>\n<option value="janowski">janowski</option>\n<option value="krasnostawski">krasnostawski</option>\n<option value="krasnicki">kra\u015bnicki</option>\n<option value="lubartowski">lubartowski</option>\n<option value="lubelski">lubelski</option>\n<option value="leczynski">\u0142\u0119czy\u0144ski</option>\n<option value="lukowski">\u0142ukowski</option>\n<option value="opolski">opolski</option>\n<option value="parczewski">parczewski</option>\n<option value="pulawski">pu\u0142awski</option>\n<option value="radzynski">radzy\u0144ski</option>\n<option value="rycki">rycki</option>\n<option value="swidnicki">\u015bwidnicki</option>\n<option value="tomaszowski">tomaszowski</option>\n<option value="wlodawski">w\u0142odawski</option>\n<option value="zamojski">zamojski</option>\n<option value="gorzow-wielkopolski">Gorz\xf3w Wielkopolski</option>\n<option value="zielona-gora">Zielona G\xf3ra</option>\n<option value="gorzowski">gorzowski</option>\n<option value="krosnienski">kro\u015bnie\u0144ski</option>\n<option value="miedzyrzecki">mi\u0119dzyrzecki</option>\n<option value="nowosolski">nowosolski</option>\n<option value="slubicki">s\u0142ubicki</option>\n<option value="strzelecko-drezdenecki">strzelecko-drezdenecki</option>\n<option value="sulecinski">sule\u0144ci\u0144ski</option>\n<option value="swiebodzinski">\u015bwiebodzi\u0144ski</option>\n<option value="wschowski">wschowski</option>\n<option value="zielonogorski">zielonog\xf3rski</option>\n<option value="zaganski">\u017caga\u0144ski</option>\n<option value="zarski">\u017carski</option>\n<option value="lodz">\u0141\xf3d\u017a</option>\n<option value="piotrkow-trybunalski">Piotrk\xf3w Trybunalski</option>\n<option value="skierniewice">Skierniewice</option>\n<option value="belchatowski">be\u0142chatowski</option>\n<option value="brzezinski">brzezi\u0144ski</option>\n<option value="kutnowski">kutnowski</option>\n<option value="laski">\u0142aski</option>\n<option value="leczycki">\u0142\u0119czycki</option>\n<option value="lowicki">\u0142owicki</option>\n<option value="lodzki wschodni">\u0142\xf3dzki wschodni</option>\n<option value="opoczynski">opoczy\u0144ski</option>\n<option value="pabianicki">pabianicki</option>\n<option value="pajeczanski">paj\u0119cza\u0144ski</option>\n<option value="piotrkowski">piotrkowski</option>\n<option value="poddebicki">podd\u0119bicki</option>\n<option value="radomszczanski">radomszcza\u0144ski</option>\n<option value="rawski">rawski</option>\n<option value="sieradzki">sieradzki</option>\n<option value="skierniewicki">skierniewicki</option>\n<option value="tomaszowski">tomaszowski</option>\n<option value="wielunski">wielu\u0144ski</option>\n<option value="wieruszowski">wieruszowski</option>\n<option value="zdunskowolski">zdu\u0144skowolski</option>\n<option value="zgierski">zgierski</option>\n<option value="krakow">Krak\xf3w</option>\n<option value="tarnow">Tarn\xf3w</option>\n<option value="nowy-sacz">Nowy S\u0105cz</option>\n<option value="bochenski">boche\u0144ski</option>\n<option value="brzeski">brzeski</option>\n<option value="chrzanowski">chrzanowski</option>\n<option value="dabrowski">d\u0105browski</option>\n<option value="gorlicki">gorlicki</option>\n<option value="krakowski">krakowski</option>\n<option value="limanowski">limanowski</option>\n<option value="miechowski">miechowski</option>\n<option value="myslenicki">my\u015blenicki</option>\n<option value="nowosadecki">nowos\u0105decki</option>\n<option value="nowotarski">nowotarski</option>\n<option value="olkuski">olkuski</option>\n<option value="oswiecimski">o\u015bwi\u0119cimski</option>\n<option value="proszowicki">proszowicki</option>\n<option value="suski">suski</option>\n<option value="tarnowski">tarnowski</option>\n<option value="tatrzanski">tatrza\u0144ski</option>\n<option value="wadowicki">wadowicki</option>\n<option value="wielicki">wielicki</option>\n<option value="warszawa">Warszawa</option>\n<option value="ostroleka">Ostro\u0142\u0119ka</option>\n<option value="plock">P\u0142ock</option>\n<option value="radom">Radom</option>\n<option value="siedlce">Siedlce</option>\n<option value="bialobrzeski">bia\u0142obrzeski</option>\n<option value="ciechanowski">ciechanowski</option>\n<option value="garwolinski">garwoli\u0144ski</option>\n<option value="gostyninski">gostyni\u0144ski</option>\n<option value="grodziski">grodziski</option>\n<option value="grojecki">gr\xf3jecki</option>\n<option value="kozienicki">kozenicki</option>\n<option value="legionowski">legionowski</option>\n<option value="lipski">lipski</option>\n<option value="losicki">\u0142osicki</option>\n<option value="makowski">makowski</option>\n<option value="minski">mi\u0144ski</option>\n<option value="mlawski">m\u0142awski</option>\n<option value="nowodworski">nowodworski</option>\n<option value="ostrolecki">ostro\u0142\u0119cki</option>\n<option value="ostrowski">ostrowski</option>\n<option value="otwocki">otwocki</option>\n<option value="piaseczynski">piaseczy\u0144ski</option>\n<option value="plocki">p\u0142ocki</option>\n<option value="plonski">p\u0142o\u0144ski</option>\n<option value="pruszkowski">pruszkowski</option>\n<option value="przasnyski">przasnyski</option>\n<option value="przysuski">przysuski</option>\n<option value="pultuski">pu\u0142tuski</option>\n<option value="radomski">radomski</option>\n<option value="siedlecki">siedlecki</option>\n<option value="sierpecki">sierpecki</option>\n<option value="sochaczewski">sochaczewski</option>\n<option value="sokolowski">soko\u0142owski</option>\n<option value="szydlowiecki">szyd\u0142owiecki</option>\n<option value="warszawski-zachodni">warszawski zachodni</option>\n<option value="wegrowski">w\u0119growski</option>\n<option value="wolominski">wo\u0142omi\u0144ski</option>\n<option value="wyszkowski">wyszkowski</option>\n<option value="zwolenski">zwole\u0144ski</option>\n<option value="zurominski">\u017curomi\u0144ski</option>\n<option value="zyrardowski">\u017cyrardowski</option>\n<option value="opole">Opole</option>\n<option value="brzeski">brzeski</option>\n<option value="glubczycki">g\u0142ubczyski</option>\n<option value="kedzierzynsko-kozielski">k\u0119dzierzy\u0144ski-kozielski</option>\n<option value="kluczborski">kluczborski</option>\n<option value="krapkowicki">krapkowicki</option>\n<option value="namyslowski">namys\u0142owski</option>\n<option value="nyski">nyski</option>\n<option value="oleski">oleski</option>\n<option value="opolski">opolski</option>\n<option value="prudnicki">prudnicki</option>\n<option value="strzelecki">strzelecki</option>\n<option value="rzeszow">Rzesz\xf3w</option>\n<option value="krosno">Krosno</option>\n<option value="przemysl">Przemy\u015bl</option>\n<option value="tarnobrzeg">Tarnobrzeg</option>\n<option value="bieszczadzki">bieszczadzki</option>\n<option value="brzozowski">brzozowski</option>\n<option value="debicki">d\u0119bicki</option>\n<option value="jaroslawski">jaros\u0142awski</option>\n<option value="jasielski">jasielski</option>\n<option value="kolbuszowski">kolbuszowski</option>\n<option value="krosnienski">kro\u015bnie\u0144ski</option>\n<option value="leski">leski</option>\n<option value="lezajski">le\u017cajski</option>\n<option value="lubaczowski">lubaczowski</option>\n<option value="lancucki">\u0142a\u0144cucki</option>\n<option value="mielecki">mielecki</option>\n<option value="nizanski">ni\u017ca\u0144ski</option>\n<option value="przemyski">przemyski</option>\n<option value="przeworski">przeworski</option>\n<option value="ropczycko-sedziszowski">ropczycko-s\u0119dziszowski</option>\n<option value="rzeszowski">rzeszowski</option>\n<option value="sanocki">sanocki</option>\n<option value="stalowowolski">stalowowolski</option>\n<option value="strzyzowski">strzy\u017cowski</option>\n<option value="tarnobrzeski">tarnobrzeski</option>\n<option value="bialystok">Bia\u0142ystok</option>\n<option value="lomza">\u0141om\u017ca</option>\n<option value="suwalki">Suwa\u0142ki</option>\n<option value="augustowski">augustowski</option>\n<option value="bialostocki">bia\u0142ostocki</option>\n<option value="bielski">bielski</option>\n<option value="grajewski">grajewski</option>\n<option value="hajnowski">hajnowski</option>\n<option value="kolnenski">kolne\u0144ski</option>\n<option value="\u0142omzynski">\u0142om\u017cy\u0144ski</option>\n<option value="moniecki">moniecki</option>\n<option value="sejnenski">sejne\u0144ski</option>\n<option value="siemiatycki">siematycki</option>\n<option value="sokolski">sok\xf3lski</option>\n<option value="suwalski">suwalski</option>\n<option value="wysokomazowiecki">wysokomazowiecki</option>\n<option value="zambrowski">zambrowski</option>\n<option value="gdansk">Gda\u0144sk</option>\n<option value="gdynia">Gdynia</option>\n<option value="slupsk">S\u0142upsk</option>\n<option value="sopot">Sopot</option>\n<option value="bytowski">bytowski</option>\n<option value="chojnicki">chojnicki</option>\n<option value="czluchowski">cz\u0142uchowski</option>\n<option value="kartuski">kartuski</option>\n<option value="koscierski">ko\u015bcierski</option>\n<option value="kwidzynski">kwidzy\u0144ski</option>\n<option value="leborski">l\u0119borski</option>\n<option value="malborski">malborski</option>\n<option value="nowodworski">nowodworski</option>\n<option value="gdanski">gda\u0144ski</option>\n<option value="pucki">pucki</option>\n<option value="slupski">s\u0142upski</option>\n<option value="starogardzki">starogardzki</option>\n<option value="sztumski">sztumski</option>\n<option value="tczewski">tczewski</option>\n<option value="wejherowski">wejcherowski</option>\n<option value="katowice" selected="selected">Katowice</option>\n<option value="bielsko-biala">Bielsko-Bia\u0142a</option>\n<option value="bytom">Bytom</option>\n<option value="chorzow">Chorz\xf3w</option>\n<option value="czestochowa">Cz\u0119stochowa</option>\n<option value="dabrowa-gornicza">D\u0105browa G\xf3rnicza</option>\n<option value="gliwice">Gliwice</option>\n<option value="jastrzebie-zdroj">Jastrz\u0119bie Zdr\xf3j</option>\n<option value="jaworzno">Jaworzno</option>\n<option value="myslowice">Mys\u0142owice</option>\n<option value="piekary-slaskie">Piekary \u015al\u0105skie</option>\n<option value="ruda-slaska">Ruda \u015al\u0105ska</option>\n<option value="rybnik">Rybnik</option>\n<option value="siemianowice-slaskie">Siemianowice \u015al\u0105skie</option>\n<option value="sosnowiec">Sosnowiec</option>\n<option value="swietochlowice">\u015awi\u0119toch\u0142owice</option>\n<option value="tychy">Tychy</option>\n<option value="zabrze">Zabrze</option>\n<option value="zory">\u017bory</option>\n<option value="bedzinski">b\u0119dzi\u0144ski</option>\n<option value="bielski">bielski</option>\n<option value="bierunsko-ledzinski">bieru\u0144sko-l\u0119dzi\u0144ski</option>\n<option value="cieszynski">cieszy\u0144ski</option>\n<option value="czestochowski">cz\u0119stochowski</option>\n<option value="gliwicki">gliwicki</option>\n<option value="klobucki">k\u0142obucki</option>\n<option value="lubliniecki">lubliniecki</option>\n<option value="mikolowski">miko\u0142owski</option>\n<option value="myszkowski">myszkowski</option>\n<option value="pszczynski">pszczy\u0144ski</option>\n<option value="raciborski">raciborski</option>\n<option value="rybnicki">rybnicki</option>\n<option value="tarnogorski">tarnog\xf3rski</option>\n<option value="wodzislawski">wodzis\u0142awski</option>\n<option value="zawiercianski">zawiercia\u0144ski</option>\n<option value="zywiecki">\u017cywiecki</option>\n<option value="kielce">Kielce</option>\n<option value="buski">buski</option>\n<option value="jedrzejowski">j\u0119drzejowski</option>\n<option value="kazimierski">kazimierski</option>\n<option value="kielecki">kielecki</option>\n<option value="konecki">konecki</option>\n<option value="opatowski">opatowski</option>\n<option value="ostrowiecki">ostrowiecki</option>\n<option value="pinczowski">pi\u0144czowski</option>\n<option value="sandomierski">sandomierski</option>\n<option value="skarzyski">skar\u017cyski</option>\n<option value="starachowicki">starachowicki</option>\n<option value="staszowski">staszowski</option>\n<option value="wloszczowski">w\u0142oszczowski</option>\n<option value="olsztyn">Olsztyn</option>\n<option value="elblag">Elbl\u0105g</option>\n<option value="bartoszycki">bartoszycki</option>\n<option value="braniewski">braniewski</option>\n<option value="dzialdowski">dzia\u0142dowski</option>\n<option value="elblaski">elbl\u0105ski</option>\n<option value="elcki">e\u0142cki</option>\n<option value="gizycki">gi\u017cycki</option>\n<option value="goldapski">go\u0142dapski</option>\n<option value="ilawski">i\u0142awski</option>\n<option value="ketrzynski">k\u0119trzy\u0144ski</option>\n<option value="lidzbarski">lidzbarski</option>\n<option value="mragowski">mr\u0105gowski</option>\n<option value="nidzicki">nidzicki</option>\n<option value="nowomiejski">nowomiejski</option>\n<option value="olecki">olecki</option>\n<option value="olsztynski">olszty\u0144ski</option>\n<option value="ostrodzki">ostr\xf3dzki</option>\n<option value="piski">piski</option>\n<option value="szczycienski">szczycie\u0144ski</option>\n<option value="wegorzewski">w\u0119gorzewski</option>\n<option value="poznan">Pozna\u0144</option>\n<option value="kalisz">Kalisz</option>\n<option value="konin">Konin</option>\n<option value="leszno">Leszno</option>\n<option value="chodzieski">chodziejski</option>\n<option value="czarnkowsko-trzcianecki">czarnkowsko-trzcianecki</option>\n<option value="gnieznienski">gnie\u017anie\u0144ski</option>\n<option value="gostynski">gosty\u0144ski</option>\n<option value="grodziski">grodziski</option>\n<option value="jarocinski">jaroci\u0144ski</option>\n<option value="kaliski">kaliski</option>\n<option value="kepinski">k\u0119pi\u0144ski</option>\n<option value="kolski">kolski</option>\n<option value="koninski">koni\u0144ski</option>\n<option value="koscianski">ko\u015bcia\u0144ski</option>\n<option value="krotoszynski">krotoszy\u0144ski</option>\n<option value="leszczynski">leszczy\u0144ski</option>\n<option value="miedzychodzki">mi\u0119dzychodzki</option>\n<option value="nowotomyski">nowotomyski</option>\n<option value="obornicki">obornicki</option>\n<option value="ostrowski">ostrowski</option>\n<option value="ostrzeszowski">ostrzeszowski</option>\n<option value="pilski">pilski</option>\n<option value="pleszewski">pleszewski</option>\n<option value="poznanski">pozna\u0144ski</option>\n<option value="rawicki">rawicki</option>\n<option value="slupecki">s\u0142upecki</option>\n<option value="szamotulski">szamotulski</option>\n<option value="sredzki">\u015bredzki</option>\n<option value="sremski">\u015bremski</option>\n<option value="turecki">turecki</option>\n<option value="wagrowiecki">w\u0105growiecki</option>\n<option value="wolsztynski">wolszty\u0144ski</option>\n<option value="wrzesinski">wrzesi\u0144ski</option>\n<option value="zlotowski">z\u0142otowski</option>\n<option value="bialogardzki">bia\u0142ogardzki</option>\n<option value="choszczenski">choszcze\u0144ski</option>\n<option value="drawski">drawski</option>\n<option value="goleniowski">goleniowski</option>\n<option value="gryficki">gryficki</option>\n<option value="gryfinski">gryfi\u0144ski</option>\n<option value="kamienski">kamie\u0144ski</option>\n<option value="kolobrzeski">ko\u0142obrzeski</option>\n<option value="koszalinski">koszali\u0144ski</option>\n<option value="lobeski">\u0142obeski</option>\n<option value="mysliborski">my\u015bliborski</option>\n<option value="policki">policki</option>\n<option value="pyrzycki">pyrzycki</option>\n<option value="slawienski">s\u0142awie\u0144ski</option>\n<option value="stargardzki">stargardzki</option>\n<option value="szczecinecki">szczecinecki</option>\n<option value="swidwinski">\u015bwidwi\u0144ski</option>\n<option value="walecki">wa\u0142ecki</option>\n</select>'

# PLPostalCodeField ##############################################################

>>> from django.contrib.localflavor.pl.forms import PLPostalCodeField
>>> f = PLPostalCodeField()
>>> f.clean('43--434')
Traceback (most recent call last):
...
ValidationError: [u'Enter a postal code in the format XX-XXX.']
>>> f.clean('41-403')
u'41-403'

# PLNIPField ###############################################################

>>> from django.contrib.localflavor.pl.forms import PLNIPField
>>> f = PLNIPField()
>>> f.clean('43-343-234-323')
Traceback (most recent call last):
...
ValidationError: [u'Enter a tax number field (NIP) in the format XXX-XXX-XX-XX or XX-XX-XXX-XXX.']
>>> f.clean('64-62-414-124')
u'6462414124'
>>> f.clean('646-241-41-24')
u'6462414124'
>>> f.clean('646-241-41-23')
Traceback (most recent call last):
...
ValidationError: [u'Wrong checksum for the Tax Number (NIP).']
 
# PLPESELField ############################################

>>> from django.contrib.localflavor.pl.forms import PLPESELField
>>> f =  PLPESELField()
>>> f.clean('80071610614')
u'80071610614'
>>> f.clean('80071610610')
Traceback (most recent call last):
...
ValidationError: [u'Wrong checksum for the National Identification Number.']
>>> f.clean('80')
Traceback (most recent call last):
...
ValidationError: [u'National Identification Number consists of 11 digits.']
>>> f.clean('800716106AA')
Traceback (most recent call last):
...
ValidationError: [u'National Identification Number consists of 11 digits.']

# PLREGONField ################################################

>>> from django.contrib.localflavor.pl.forms import PLREGONField
>>> f = PLREGONField()
>>> f.clean('12345678512347')
u'12345678512347'
>>> f.clean('590096454')
u'590096454'
>>> f.clean('123456784')
Traceback (most recent call last):
...
ValidationError: [u'Wrong checksum for the National Business Register Number (REGON).']
>>> f.clean('12345678412342')
Traceback (most recent call last):
...
ValidationError: [u'Wrong checksum for the National Business Register Number (REGON).']
>>> f.clean('590096453')
Traceback (most recent call last):
...
ValidationError: [u'Wrong checksum for the National Business Register Number (REGON).']
>>> f.clean('590096')
Traceback (most recent call last):
...
ValidationError: [u'National Business Register Number (REGON) consists of 9 or 14 digits.']

"""
