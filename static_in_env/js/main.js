jQuery(function($) {

	$('.parent-search').on("focus", function(e){
		console.log('focus got called');
		$('.search-dropdown').addClass('active');
	});

	$(document).on("click", function(e){
		const searchDropDown = $('.search-dropdown');
		const parentSearch = $('.parent-search');
		if (!searchDropDown.is(e.target) && searchDropDown.has(e.target).length === 0 && !parentSearch.is(e.target) && !parentSearch.has(e.target).length) 
		{
			searchDropDown.removeClass('active');
		}
	});

	$(".increament-input").on("click", function(e){
		e.preventDefault();
		let val = $(this).parent().siblings('.incremental-value').first().val() ?? 0;
		val = Number(val) + 1;
		$(this).parent().siblings('.incremental-value').first().val(val);
	})

	$(".decreament-input").on("click", function(e){
		e.preventDefault();
		let val = $(this).parent().siblings('.incremental-value').first().val() ?? 0;
		if(val > 1) {
			val = Number(val) - 1;
		}
		$(this).parent().siblings('.incremental-value').first().val(val);
	})

	$(".accept-cookie").on("click", function(e){
		e.preventDefault();
		//handle cookie permission here
		$(".cookie-box").hide();
	});

	var scroll  = 0;

	$(window).scroll(function(e){
		console.log("scrolling");
		scroll = $(window).scrollTop();
		if(scroll > 200) {
			$(".scroll-container").show();
		} else {
			$(".scroll-container").hide();
		}
	});

	$(".scroll-top").on("click", function(e){
		e.preventDefault();
		window.scroll({
			top: 0, 
			left: 0, 
			behavior: 'smooth'
		  });
	});

	$(".scroll-bottom").on("click", function(e){
		e.preventDefault();
		window.scrollTo(scroll,document.body.scrollHeight);
	});

});
