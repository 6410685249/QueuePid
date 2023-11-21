const findMyState = () => {
    const status = document.querySelector('.status');

    const success = (position) => {
        console.log(position)
        const latitude = position.coords.latitude;
        const longutude = position.coords.longitude;
        console.log(latitude + longutude)
    }
    const error = () => {
        status.textContent = 'Unable to retrieve your location'
    }
    

}

document.querySelector('.find-state').addEventListener('click',findMyState)