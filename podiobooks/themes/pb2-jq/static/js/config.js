function siteVars(opt){
	switch (opt){
		case 'home':
			return '/';
			break;
		case 'theme':
			return '/assets/static/';
			break;
		case 'img':
			return siteVars('theme') + 'images/';
			break; 
		case 'swf':
			return siteVars('theme') + 'swf/';
			break; 
		default:
			return null;
			break;
	}
}