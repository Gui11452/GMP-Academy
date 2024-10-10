(function(){

    const formRegistro = document.querySelector('.registro form');
    const senha1Input = document.querySelector('#senha1');
    const senha2Input = document.querySelector('#senha2');

    const senha1Errors = document.querySelector('.senha1-errors');
    const senha2Errors = document.querySelector('.senha2-errors');

    const loader = document.querySelector('.loader');
    const buttonSubmit = document.querySelector('#submit');

    formRegistro.addEventListener('submit', e => {

        let validador = true;

        senha1Errors.innerHTML = '';
        senha2Errors.innerHTML = '';

        senha1Errors.style.display = 'none';
        senha2Errors.style.display = 'none';

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