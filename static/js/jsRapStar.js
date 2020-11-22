(function($){
	$.fn.jsRapStar = function(options){
		
		return this.each(function(){
			let value = $(this).attr('value');
			let color = $(this).attr('color');
			value = value === undefined ? 0 : parseFloat(value);
			color = color === undefined ? 'yellow' : color;
			this.opt = $.extend({
				star:'&#9733',
				colorFront:color,
				colorBack:'white',
				enabled:true,
				step:true,
				starHeight:16,
				length:6,
				value: value,
				onClick:null,
				onMousemove:null,
				onMouseleave:null
			},options);
			const base = this;
			const starH = Array(this.opt.length + 1).join('<span>' + this.opt.star + '</span>');
			this.StarB = $(this).addClass('rapStar').css({color:this.opt.colorBack,'font-size':this.opt.starHeight + 'px'}).html(starH);
			const sw = this.StarB.width() / this.opt.length;
			let aw = base.opt.value * sw;
			this.StarF = $('<div>').addClass('rapStarFront').css({color:this.opt.colorFront}).html(starH).width(aw).appendTo(this);
			if(this.opt.enabled){
				$(this).bind({
					mousemove:function(e){
						e.preventDefault();
						const relativeX = e.clientX - $(base)[0].getBoundingClientRect().left;
						var e = Math.floor(relativeX / sw) + 1;
						if(base.opt.step) newWidth = e * sw;
						else newWidth = relativeX;
						this.StarF.width(newWidth);
						if(base.opt.onMousemove)
							base.opt.onMousemove.call(base, Math.round(10 * newWidth / sw));
					},
					mouseleave:function(e){
						this.StarF.width(aw);
						if(base.opt.onMouseleave)
							base.opt.onMouseleave.call(base,base.opt.value);
					},
					click:function(e){
						e.preventDefault();
						aw = newWidth;
						this.StarF.width(newWidth);
						base.opt.value = Math.round(10 * newWidth / sw);
						if(base.opt.onClick)
							base.opt.onClick.call(base,base.opt.value);
					}
				});
			}else
				$(this).addClass('rapStarDisable');
		})
	}
})(jQuery);
