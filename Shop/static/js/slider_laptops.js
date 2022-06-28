$(document).ready(function() {
    let position = 0;
    const slidesToShow = 4;
    const slidesToScroll = 2;
    const container = $('.slider-container');
    const track = $('.track-laptops');
    const item = $('.item-laptops');
    const btnPrev = $('.btn-prev-laptops');
    const btnNext = $('.btn-next-laptops');
    const itemsCount = item.length;

    const itemWidth = container.width() / slidesToShow;
    const movePosition = slidesToScroll * itemWidth;

    item.each(function(home, item) {
        $(item).css({
            minWidth: itemWidth,
        });
    });

    btnPrev.click(function() {
        const itemsLeft = Math.abs(position) / itemWidth;

        position += itemsLeft >= slidesToScroll ? movePosition : itemsLeft * itemWidth;
        setPosition();
        checkBtns();
    });

    btnNext.click(function() {
        let itemsLeft = itemsCount - (Math.abs(position) + slidesToShow * itemWidth) / itemWidth;
        position -= itemsLeft >= slidesToScroll ? movePosition : itemsLeft * itemWidth;

        setPosition();
        checkBtns();
    });

    const setPosition = () => {
        track.css({
            transform: `translateX(${position}px)`
        });
    };

    const checkBtns = () => {
        btnPrev.prop('disabled', position === 0);
        btnNext.prop('disabled', position <= -(itemsCount - slidesToShow) * itemWidth);
    };

    checkBtns();

});