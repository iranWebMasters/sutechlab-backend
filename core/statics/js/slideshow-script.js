"use strict";
(function () {
	// Global variables
	var userAgent = navigator.userAgent.toLowerCase(),
		initialDate = new Date(),

		$document = $( document ),
		$window = $( window ),
		$html = $( "html" ),
		$body = $( "body" ),

		isDesktop = $html.hasClass( "desktop" ),
		isIE = userAgent.indexOf( "msie" ) !== -1 ? parseInt( userAgent.split( "msie" )[ 1 ], 10 ) : userAgent.indexOf( "trident" ) !== -1 ? 11 : userAgent.indexOf( "edge" ) !== -1 ? 12 : false,
		isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test( navigator.userAgent ),
		windowReady = false,
		isNoviBuilder = false,
		loaderTimeoutId,

		plugins = {
			swiper:                  $( ".swiper-slider" ),
		};

	// Initialize scripts that require a finished document
	$( function () {
		isNoviBuilder = window.xMode;

		

		/**
		 * @desc Calculate the height of swiper slider basing on data attr
		 * @param {object} object - slider jQuery object
		 * @param {string} attr - attribute name
		 * @return {number} slider height
		 */
		function getSwiperHeight ( object, attr ) {
			var val = object.attr( "data-" + attr ),
				dim;

			if ( !val ) {
				return undefined;
			}

			dim = val.match( /(px)|(%)|(vh)|(vw)$/i );

			if ( dim.length ) {
				switch ( dim[ 0 ] ) {
					case "px":
						return parseFloat( val );
					case "vh":
						return $window.height() * (parseFloat( val ) / 100);
					case "vw":
						return $window.width() * (parseFloat( val ) / 100);
					case "%":
						return object.width() * (parseFloat( val ) / 100);
				}
			} else {
				return undefined;
			}
		}

		/**
		 * @desc Toggle swiper videos on active slides
		 * @param {object} swiper - swiper slider
		 */
		function toggleSwiperInnerVideos ( swiper ) {
			var prevSlide = $( swiper.slides[ swiper.previousIndex ] ),
				nextSlide = $( swiper.slides[ swiper.activeIndex ] ),
				videos,
				videoItems = prevSlide.find( "video" );

			for ( var i = 0; i < videoItems.length; i++ ) {
				videoItems[ i ].pause();
			}

			videos = nextSlide.find( "video" );
			if ( videos.length ) {
				videos.get( 0 ).play();
			}
		}

		/**
		 * @desc Toggle swiper animations on active slides
		 * @param {object} swiper - swiper slider
		 */
		function toggleSwiperCaptionAnimation ( swiper ) {
			var prevSlide = $( swiper.container ).find( "[data-caption-animate]" ),
				nextSlide = $( swiper.slides[ swiper.activeIndex ] ).find( "[data-caption-animate]" ),
				delay,
				duration,
				nextSlideItem,
				prevSlideItem;

			for ( var i = 0; i < prevSlide.length; i++ ) {
				prevSlideItem = $( prevSlide[ i ] );

				prevSlideItem.removeClass( "animated" )
					.removeClass( prevSlideItem.attr( "data-caption-animate" ) )
					.addClass( "not-animated" );
			}


			var tempFunction = function ( nextSlideItem, duration ) {
				return function () {
					nextSlideItem
						.removeClass( "not-animated" )
						.addClass( nextSlideItem.attr( "data-caption-animate" ) )
						.addClass( "animated" );
					if ( duration ) {
						nextSlideItem.css( 'animation-duration', duration + 'ms' );
					}
				};
			};

			for ( var i = 0; i < nextSlide.length; i++ ) {
				nextSlideItem = $( nextSlide[ i ] );
				delay = nextSlideItem.attr( "data-caption-delay" );
				duration = nextSlideItem.attr( 'data-caption-duration' );
				if ( !isNoviBuilder ) {
					if ( delay ) {
						setTimeout( tempFunction( nextSlideItem, duration ), parseInt( delay, 10 ) );
					} else {
						tempFunction( nextSlideItem, duration );
					}

				} else {
					nextSlideItem.removeClass( "not-animated" )
				}
			}
		}


		// Additional class on html if mac os.
		if ( navigator.platform.match( /(Mac)/i ) ) {
			$html.addClass( "mac-os" );
		}

		// Adds some loosing functionality to IE browsers (IE Polyfills)
		if (isIE) {
			if (isIE === 12) $html.addClass("ie-edge");
			if (isIE === 11) $html.addClass("ie-11");
			if (isIE < 10) $html.addClass("lt-ie-10");
			if (isIE < 11) $html.addClass("ie-10");
		}

		
		function formatIndex ( index ) {
			return index < 10 ? '0' + index : index;
		}

		// Swiper
		if ( plugins.swiper.length ) {
			for ( var i = 0; i < plugins.swiper.length; i++ ) {
				var s = $( plugins.swiper[ i ] );
				var pag = s.find( ".swiper-pagination" ),
					next = s.find( ".swiper-button-next" ),
					prev = s.find( ".swiper-button-prev" ),
					bar = s.find( ".swiper-scrollbar" ),
					swiperSlide = s.find( ".swiper-slide" ),
					autoplay = false;

				for ( var j = 0; j < swiperSlide.length; j++ ) {
					var $this = $( swiperSlide[ j ] ),
						url;

					if ( url = $this.attr( "data-slide-bg" ) ) {
						$this.css( {
							"background-image": "url(" + url + ")",
							"background-size":  "cover"
						} )
					}
				}

				swiperSlide.end()
					.find( "[data-caption-animate]" )
					.addClass( "not-animated" )
					.end();

				s.swiper( {
					autoplay:                 s.attr( 'data-autoplay' ) ? s.attr( 'data-autoplay' ) === "false" ? undefined : s.attr( 'data-autoplay' ) : 5000,
					direction:                s.attr( 'data-direction' ) && isDesktop ? s.attr( 'data-direction' ) : "horizontal",
					effect:                   s.attr( 'data-slide-effect' ) ? s.attr( 'data-slide-effect' ) : "slide",
					speed:                    s.attr( 'data-slide-speed' ) ? s.attr( 'data-slide-speed' ) : 600,
					keyboardControl:          s.attr( 'data-keyboard' ) === "true",
					mousewheelControl:        s.attr( 'data-mousewheel' ) === "true",
					mousewheelReleaseOnEdges: s.attr( 'data-mousewheel-release' ) === "true",
					nextButton:               next.length ? next.get( 0 ) : null,
					prevButton:               prev.length ? prev.get( 0 ) : null,
					pagination:               pag.length ? pag.get( 0 ) : null,
					paginationClickable:      pag.length ? pag.attr( "data-clickable" ) !== "false" : false,
					paginationBulletRender:   function ( swiper, index, className ) {
						if ( pag.attr( "data-index-bullet" ) === "true" ) {
							return '<span class="' + className + '">' + (index + 1) + '</span>';
						} else if ( pag.attr( "data-bullet-custom" ) === "true" ) {
							return '<span class="' + className + '"><span></span></span>';
						} else {
							return '<span class="' + className + '"></span>';
						}
					},
					scrollbar:                bar.length ? bar.get( 0 ) : null,
					scrollbarDraggable:       bar.length ? bar.attr( "data-draggable" ) !== "false" : true,
					scrollbarHide:            bar.length ? bar.attr( "data-draggable" ) === "false" : false,
					loop:                     isNoviBuilder ? false : s.attr( 'data-loop' ) !== "false",
					simulateTouch:            s.attr( 'data-simulate-touch' ) && !isNoviBuilder ? s.attr( 'data-simulate-touch' ) === "true" : false,
					onTransitionStart:        function ( swiper ) {
						toggleSwiperInnerVideos( swiper );
					},
					onTransitionEnd:          function ( swiper ) {
						toggleSwiperCaptionAnimation( swiper );
					},
					onInit:                   (function ( s ) {
						return function ( swiper ) {
							toggleSwiperInnerVideos( swiper );
							toggleSwiperCaptionAnimation( swiper );

							var $swiper = $( s );

							var swiperCustomIndex = $swiper.find( '.swiper-pagination__fraction-index' ).get( 0 ),
								swiperCustomCount = $swiper.find( '.swiper-pagination__fraction-count' ).get( 0 );

							if ( swiperCustomIndex && swiperCustomCount ) {
								swiperCustomIndex.innerHTML = formatIndex( swiper.realIndex + 1 );
								if ( swiperCustomCount ) {
									if ( isNoviBuilder ? false : s.attr( 'data-loop' ) !== "false" ) {
										swiperCustomCount.innerHTML = formatIndex( swiper.slides.length - 2 );
									} else {
										swiperCustomCount.innerHTML = formatIndex( swiper.slides.length );
									}
								}
							}
						}
					}( s )),
					onSlideChangeStart:       (function ( s ) {
						return function ( swiper ) {
							var swiperCustomIndex = $( s ).find( '.swiper-pagination__fraction-index' ).get( 0 );

							if ( swiperCustomIndex ) {
								swiperCustomIndex.innerHTML = formatIndex( swiper.realIndex + 1 );
							}
						}
					}( s ))
				} );

				$window.on( "resize", (function ( s ) {
					return function () {
						var mh = getSwiperHeight( s, "min-height" ),
							h = getSwiperHeight( s, "height" );
						if ( h ) {
							s.css( "height", mh ? mh > h ? mh : h : h );
						}
					}
				})( s ) ).trigger( "resize" );
			}
		}
	} );
}());