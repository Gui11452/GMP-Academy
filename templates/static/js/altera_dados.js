(function(){

    const formRegistro = document.querySelector('.registro form');
    const userInput = document.querySelector('#user');
    const emailInput = document.querySelector('#email');
    const nameInput = document.querySelector('#name');

    const userErrors = document.querySelector('.user-errors');
    const emailErrors = document.querySelector('.email-errors');
    const nameErrors = document.querySelector('.name-errors');

    const loader = document.querySelector('.loader');
    const buttonSubmit = document.querySelector('#submit');

    formRegistro.addEventListener('submit', e => {

        let validador = true;

        userErrors.innerHTML = '';
        emailErrors.innerHTML = '';
        nameErrors.innerHTML = '';

        userErrors.style.display = 'none';
        emailErrors.style.display = 'none';
        nameErrors.style.display = 'none';

        if(!nameInput.value){
            nameErrors.innerHTML = 'Esse campo não pode ficar vazio!';
            nameErrors.style.display = 'block';
            validador = false;
        }

        if(!userInput.value){
            userErrors.innerHTML = 'Esse campo não pode ficar vazio!';
            userErrors.style.display = 'block';
            validador = false;
        }

        if(!emailInput.value){
            emailErrors.innerHTML = 'Esse campo não pode ficar vazio!';
            emailErrors.style.display = 'block';
            validador = false;
        }

        if(!validador){
            e.preventDefault(); 
        } else{
            buttonSubmit.style.display = 'none';
            loader.style.display = 'inline-block';
        }

    });

})();