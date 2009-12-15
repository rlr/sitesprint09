var rr = window.rr || {};

rr.home = (function($){
	
	function init() {
		$('#main div.twitter p.text').each(function(){
			var $this = $(this);
			$this.html(ify.clean($this.html()))
		});
	}
	
	return {
		init: init
	};
})(jQuery);

jQuery(rr.home.init);
