(function(){

    const alternativa = document.querySelectorAll('.alternativas');
    const alternativaI = document.querySelectorAll('.alternativa i');
    const alternativaP = document.querySelectorAll('.alternativa p');
    const alternativaSpan = document.querySelectorAll('.alternativa span');
    const alternativaLabel = document.querySelectorAll('.alternativa label');
    const alternativaInput = document.querySelectorAll('.alternativa input');

    const gabaritoInput = document.querySelector('.gabarito input');

    const questoesForm = document.querySelector('.questoes form');

    const abaComunidade = document.querySelectorAll('.aba-comunidade p');
    const [botaoComentario, botaoDuvida, botaoReportarDuvidaProfessor] = abaComunidade;

    const comentarios = document.querySelector('.comentarios');
    const duvidas = document.querySelector('.duvidas');
    const duvidasProfessor = document.querySelector('.duvidas_professor');

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == botaoComentario){
            botaoComentario.classList.add('selecionado');
            botaoDuvida.classList.remove('selecionado');
            botaoReportarDuvidaProfessor.classList.remove('selecionado');

            comentarios.classList.add('desocultar');
            duvidas.classList.remove('desocultar');
            duvidasProfessor.classList.remove('desocultar');
            return;
        }
        else if(el == botaoDuvida){
            botaoComentario.classList.remove('selecionado');
            botaoDuvida.classList.add('selecionado');
            botaoReportarDuvidaProfessor.classList.remove('selecionado');

            comentarios.classList.remove('desocultar');
            duvidas.classList.add('desocultar');
            duvidasProfessor.classList.remove('desocultar');
            return;
        }
        else if(el == botaoReportarDuvidaProfessor){
            botaoComentario.classList.remove('selecionado');
            botaoDuvida.classList.remove('selecionado');
            botaoReportarDuvidaProfessor.classList.add('selecionado');

            comentarios.classList.remove('desocultar');
            duvidas.classList.remove('desocultar');
            duvidasProfessor.classList.add('desocultar');
            return;
        }

        for(let y = 0; y < alternativaI.length; y++){
            if(alternativaI[y] == el){
                alternativaP[y].classList.toggle('cortado');
                alternativaI[y].classList.toggle('cortado');
                alternativaSpan[y].classList.toggle('cortado');

                alternativaInput[y].checked = false;
                alternativaSpan[y].classList.remove('selecionado');
                
                let inputChecked = false;
                for(let x = 0; x < alternativaInput.length; x++){
                    if(alternativaInput[x].checked){
                        inputChecked = true;
                    }
                }
                if(!inputChecked){
                    gabaritoInput.classList.add('desabilitado');
                }

            } 
        }

    });

    questoesForm.addEventListener('submit', e => {
        if(gabaritoInput.classList.contains('desabilitado')){
            e.preventDefault();
        }
    });

    document.addEventListener('change', e => {

        const el = e.target;

        let validador = false;
        for(let y = 0; y < alternativaInput.length; y++){
            if(alternativaInput[y].checked){
                alternativaSpan[y].classList.add('selecionado');
                alternativaP[y].classList.remove('cortado');
                alternativaI[y].classList.remove('cortado');
                alternativaSpan[y].classList.remove('cortado');
                validador = true;
            } else{
                alternativaSpan[y].classList.remove('selecionado');
            }
        }
        if(validador){
            gabaritoInput.classList.remove('desabilitado');
        } else{
            gabaritoInput.classList.add('desabilitado');
        }

    });

})();