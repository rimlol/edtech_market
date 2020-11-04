(function($) {
    "use strict";
	$('#container').showmore({
		closedHeight: 250,
		buttonTextMore: 'Показать еще',
		buttonTextLess: 'Close',
		buttonCssClass: 'showmore-button',
		animationSpeed: 0.5
	});
	$('#container1').showmore({
		closedHeight: 315,
		buttonTextMore: 'Показать еще',
		buttonTextLess: 'Close',
		buttonCssClass: 'showmore-button',
		animationSpeed: 0.5
	});
	$('#container2').showmore({
		closedHeight: 280,
		buttonTextMore: 'Показать еще',
		buttonTextLess: 'Close',
		buttonCssClass: 'showmore-button',
		animationSpeed: 0.5
	});
	$('.hide-details').showmore({
		closedHeight: 137,
		buttonTextMore: 'Показать еще',
		buttonTextLess: 'Close',
		buttonCssClass: 'showmore-button1',
		animationSpeed: 0.5
	});
	$('.hide-details2').showmore({
		closedHeight: 400,
		buttonTextMore: 'Показать еще',
		buttonTextLess: 'Close',
		buttonCssClass: 'showmore-button',
		animationSpeed: 0.5
	});
	if (document.documentElement.clientWidth < 900) {
		$('#container1').showmore({
			closedHeight: 450,
			buttonTextMore: 'Показать еще',
			buttonTextLess: 'Close',
			buttonCssClass: 'showmore-button',
			animationSpeed: 0.5
		});
	}
	$( "#mySlider" ).slider({
		range: true,
		min: 1000,
		max: 500000,
		values: [ 30000, 100000 ],
		slide: function( event, ui ) {
			$( "#price" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
		}
	});

	$( "#price" ).val( "$" + $( "#mySlider" ).slider( "values", 0 ) +
			   " - $" + $( "#mySlider" ).slider( "values", 1 ) );
})(jQuery);