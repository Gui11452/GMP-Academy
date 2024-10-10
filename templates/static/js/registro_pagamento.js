(function(){

    const formRegistro = document.querySelector('#form-registro');
    const userInput = document.querySelector('#user');
    const senha1Input = document.querySelector('#senha1');
    const senha2Input = document.querySelector('#senha2');
    const emailInput = document.querySelector('#email-registro');
    const nameInput = document.querySelector('#name');

    const userErrors = document.querySelector('.user-errors');
    const senha1Errors = document.querySelector('.senha1-errors');
    const senha2Errors = document.querySelector('.senha2-errors');
    const emailErrors = document.querySelector('.email-errors');
    const nameErrors = document.querySelector('.name-errors');

    const loader = document.querySelector('.loader-registro');
    const buttonSubmit = document.querySelector('.submit-registro');

    formRegistro.addEventListener('submit', e => {

        let validador = true;e.preventDefault();

        userErrors.innerHTML = '';
        senha1Errors.innerHTML = '';
        senha2Errors.innerHTML = '';
        emailErrors.innerHTML = '';
        nameErrors.innerHTML = '';

        userErrors.style.display = 'none';
        senha1Errors.style.display = 'none';
        senha2Errors.style.display = 'none';
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

        if(!senha2Input.value){
            senha2Errors.innerHTML = 'Esse campo não pode ficar vazio!';
            senha2Errors.style.display = 'block';
            validador = false;
        }

        if(!senha1Input.value){
            senha1Errors.innerHTML = 'Esse campo não pode ficar vazio!';
            senha1Errors.style.display = 'block';
            validador = false;
        }

        else if(senha1Input.value.length != senha2Input.value.length){
            senha1Errors.innerHTML = 'As senhas precisam ser iguais!';
            senha1Errors.style.display = 'block';
            validador = false;
        }

        else if(senha1Input.value.length < 8){
            senha1Errors.innerHTML = 'As senhas precisam ter no mínimo 8 caracteres!';
            senha1Errors.style.display = 'block';
            validador = false;
        }

        if(senha1Input.value.length < 8){
            userInput.innerHTML = 'O usuário precisa ter no mínimo 8 caracteres!';
            userInput.style.display = 'block';
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