$(document).ready(function() {
    let position = 0;
    const slidesToShow = 4;
    const slidesToScroll = 2;
    const container = $('.slider-container');
    const track = $('.track-phones');
    const item = $('.item-phones');
    const btnPrevPhone = $('.btn-prev-phones');
    const btnNextPhone = $('.btn-next-phones');
    const itemsCount = item.length;
    console.log(itemsCount);

    const itemWidth = container.width() / slidesToShow;
    const movePosition = slidesToScroll * itemWidth;

    item.each(function(home, item) {
        $(item).css({
            minWidth: itemWidth,
        });
    });

    btnPrevPhone.click(function() {
        const itemsLeft = Math.abs(position) / itemWidth;

        position += itemsLeft >= slidesToScroll ? movePosition : itemsLeft * itemWidth;
        setPositionPhone();
        checkBtnsPhone();
    });

    btnNextPhone.click(function() {
        let itemsLeft = itemsCount - (Math.abs(position) + slidesToShow * itemWidth) / itemWidth;
        position -= itemsLeft >= slidesToScroll ? movePosition : itemsLeft * itemWidth;

        setPositionPhone();
        checkBtnsPhone();
    });

    const setPositionPhone = () => {
        track.css({
            transform: `translateX(${position}px)`
        });
    };

    const checkBtnsPhone = () => {
        btnPrevPhone.prop('disabled', position === 0);
        btnNextPhone.prop('disabled', position <= -(itemsCount - slidesToShow) * itemWidth);
    };

    checkBtnsPhone();

});