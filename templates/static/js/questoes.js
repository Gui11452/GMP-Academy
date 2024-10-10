(function () {

    const acerteiQuestoesLabel = document.querySelectorAll('.acerto_questoes label');
    const [acerteiQuestoesLabel1, acerteiQuestoesLabel2, acerteiQuestoesLabel3, acerteiQuestoesLabel4] = acerteiQuestoesLabel;

    const filtroPalavraChaveI = document.querySelector('.filtro_palavra_chave i');
    const filtroPalavraChave = document.querySelector('.filtro_palavra_chave');
    const filtroPalavraChaveSpan = document.querySelector('.filtro_palavra_chave span');
    const filtrosSelecionados = document.querySelector('.filtros_selecionados');
    const filtrosSelecionadosP = document.querySelector('.filtros_selecionados>p');

    const palavraChave = document.querySelector('#palavra_chave');

    const buttonDisciplina = document.querySelector('.button-disciplina');
    const buttonDisciplinaI = document.querySelector('.button-disciplina i');
    const disciplinaDropdown = document.querySelector('.button-disciplina .dropdown-button');
    const disciplinaDropdownInput = document.querySelector('.button-disciplina .dropdown-button>input');
    const disciplinaDropdownLabelSpan = document.querySelectorAll('.button-disciplina .dropdown-button label span');
    const disciplinaDropdownLabel = document.querySelectorAll('.button-disciplina .dropdown-button label');
    const disciplinaDropdownLabelInput = document.querySelectorAll('.button-disciplina .dropdown-button label input');
    const disciplinaDropdownH4 = document.querySelector('.button-disciplina .dropdown-button h4');

    const buttonAno = document.querySelector('.button-ano');
    const buttonAnoI = document.querySelector('.button-ano i');
    const anoDropdown = document.querySelector('.button-ano .dropdown-button');
    const anoDropdownInput = document.querySelector('.button-ano .dropdown-button>input');
    const anoDropdownLabelSpan = document.querySelectorAll('.button-ano .dropdown-button label span');
    const anoDropdownLabel = document.querySelectorAll('.button-ano .dropdown-button label');
    const anoDropdownLabelInput = document.querySelectorAll('.button-ano .dropdown-button label input');
    const anoDropdownH4 = document.querySelector('.button-ano .dropdown-button h4');

    const buttonProva = document.querySelector('.button-prova');
    const buttonProvaI = document.querySelector('.button-prova i');
    const provaDropdown = document.querySelector('.button-prova .dropdown-button');
    const provaDropdownInput = document.querySelector('.button-prova .dropdown-button>input');
    const provaDropdownLabelSpan = document.querySelectorAll('.button-prova .dropdown-button label span');
    const provaDropdownLabel = document.querySelectorAll('.button-prova .dropdown-button label');
    const provaDropdownLabelInput = document.querySelectorAll('.button-prova .dropdown-button label input');
    const provaDropdownH4 = document.querySelector('.button-prova .dropdown-button h4');

    const buttonBanca = document.querySelector('.button-banca');
    const buttonBancaI = document.querySelector('.button-banca i');
    const bancaDropdown = document.querySelector('.button-banca .dropdown-button');
    const bancaDropdownInput = document.querySelector('.button-banca .dropdown-button>input');
    const bancaDropdownLabelSpan = document.querySelectorAll('.button-banca .dropdown-button label span');
    const bancaDropdownLabel = document.querySelectorAll('.button-banca .dropdown-button label');
    const bancaDropdownLabelInput = document.querySelectorAll('.button-banca .dropdown-button label input');
    const bancaDropdownH4 = document.querySelector('.button-banca .dropdown-button h4');

    const buttonEstado = document.querySelector('.button-estado');
    const buttonEstadoI = document.querySelector('.button-estado i');
    const estadoDropdown = document.querySelector('.button-estado .dropdown-button');
    const estadoDropdownInput = document.querySelector('.button-estado .dropdown-button>input');
    const estadoDropdownLabelSpan = document.querySelectorAll('.button-estado .dropdown-button label span');
    const estadoDropdownLabel = document.querySelectorAll('.button-estado .dropdown-button label');
    const estadoDropdownLabelInput = document.querySelectorAll('.button-estado .dropdown-button label input');
    const estadoDropdownH4 = document.querySelector('.button-estado .dropdown-button h4');

    const labelAcertoQuestoes = document.querySelectorAll('.acerto_questoes label');

    const alternativas = document.querySelectorAll('.alternativas');
    const gabaritoInput = document.querySelectorAll('.gabarito input');

    function parametrosURL() {
        const queryString = window.location.search;

        const params = new URLSearchParams(queryString);

        const palavraAcertoQuestao = params.get('acerto_questao');
        const palavraChaveValor = params.get('palavra_chave');
        const disciplinaArray = params.getAll('disciplina');
        const anoArray = params.getAll('ano');
        const provaArray = params.getAll('prova');
        const bancaArray = params.getAll('banca');
        const estadoArray = params.getAll('estado');

        if (palavraChaveValor) {
            filtroPalavraChave.style.display = 'flex';
            filtroPalavraChaveSpan.innerHTML = palavraChaveValor;
            palavraChave.value = palavraChaveValor;
            filtrosSelecionadosP.style.display = 'none';
        }

        if (palavraAcertoQuestao) {
            for (let r = 0; r < labelAcertoQuestoes.length; r++) {
                labelAcertoQuestoes[r].classList.remove('selecionado');
            }

            const acertoQuestao = document.querySelector(`#${palavraAcertoQuestao}`);
            acertoQuestao.checked = true;
            acertoQuestao.previousElementSibling.classList.add('selecionado');
        }

        for (let d = 0; d < disciplinaArray.length; d++) {
            filtrosSelecionadosP.style.display = 'none';
            const div = createDivFiltrosSelecionados(disciplinaArray[d], 'Disciplina', 'filtro_disciplina');
            filtrosSelecionados.appendChild(div);
            for (let x = 0; x < disciplinaDropdownLabelInput.length; x++) {
                if (disciplinaDropdownLabelSpan[x].innerText.trim() == disciplinaArray[d]) {
                    disciplinaDropdownLabelInput[x].checked = true;
                    continue;
                }
            }
        }

        for (let d = 0; d < anoArray.length; d++) {
            filtrosSelecionadosP.style.display = 'none';
            const div = createDivFiltrosSelecionados(anoArray[d], 'Ano', 'filtro_ano');
            filtrosSelecionados.appendChild(div);
            for (let x = 0; x < anoDropdownLabelInput.length; x++) {
                if (anoDropdownLabelSpan[x].innerText.trim() == anoArray[d]) {
                    anoDropdownLabelInput[x].checked = true;
                    continue;
                }
            }
        }

        for (let d = 0; d < provaArray.length; d++) {
            filtrosSelecionadosP.style.display = 'none';
            const div = createDivFiltrosSelecionados(provaArray[d], 'Prova', 'filtro_prova');
            filtrosSelecionados.appendChild(div);
            for (let x = 0; x < provaDropdownLabelInput.length; x++) {
                if (provaDropdownLabelSpan[x].innerText.trim() == provaArray[d]) {
                    provaDropdownLabelInput[x].checked = true;
                    continue;
                }
            }
        }

        for (let d = 0; d < bancaArray.length; d++) {
            filtrosSelecionadosP.style.display = 'none';
            const div = createDivFiltrosSelecionados(bancaArray[d], 'Banca', 'filtro_banca');
            filtrosSelecionados.appendChild(div);
            for (let x = 0; x < bancaDropdownLabelInput.length; x++) {
                if (bancaDropdownLabelSpan[x].innerText.trim() == bancaArray[d]) {
                    bancaDropdownLabelInput[x].checked = true;
                    continue;
                }
            }
        }

        for (let d = 0; d < estadoArray.length; d++) {
            filtrosSelecionadosP.style.display = 'none';
            const div = createDivFiltrosSelecionados(estadoArray[d], 'Estado', 'filtro_estado');
            filtrosSelecionados.appendChild(div);
            for (let x = 0; x < estadoDropdownLabelInput.length; x++) {
                if (estadoDropdownLabelSpan[x].innerText.trim() == estadoArray[d]) {
                    estadoDropdownLabelInput[x].checked = true;
                    continue;
                }
            }
        }

        //console.log(palavraChave);
        //console.log(disciplinaArray);
        //console.log(anoArray);
        //console.log(provaArray);
    }
    parametrosURL();

    function mensagemP() {
        let anoChecked = false;
        for (let i = 0; i < anoDropdownLabelInput.length; i++) {
            if (anoDropdownLabelInput[i].checked) {
                anoChecked = true;
                break;
            }
        }

        let provaChecked = false;
        for (let i = 0; i < provaDropdownLabelInput.length; i++) {
            if (provaDropdownLabelInput[i].checked) {
                provaChecked = true;
                break;
            }
        }

        let disciplinaChecked = false;
        for (let i = 0; i < disciplinaDropdownLabelInput.length; i++) {
            if (disciplinaDropdownLabelInput[i].checked) {
                disciplinaChecked = true;
                break;
            }
        }

        let bancaChecked = false;
        for (let i = 0; i < bancaDropdownLabelInput.length; i++) {
            if (bancaDropdownLabelInput[i].checked) {
                bancaChecked = true;
                break;
            }
        }

        let estadoChecked = false;
        for (let i = 0; i < estadoDropdownLabelInput.length; i++) {
            if (estadoDropdownLabelInput[i].checked) {
                estadoChecked = true;
                break;
            }
        }

        if (!provaChecked && !disciplinaChecked && !anoChecked  && !bancaChecked  && !estadoChecked && palavraChave.value == '') {
            filtrosSelecionadosP.style.display = 'block';
        } else {
            filtrosSelecionadosP.style.display = 'none';
        }
    }

    document.addEventListener('click', e => {

        const el = e.target;

        if (el == buttonDisciplina || el == buttonDisciplinaI) {
            disciplinaDropdown.classList.toggle('dropdown-button-desocultar');
        }

        else if (el == buttonAno || el == buttonAnoI) {
            anoDropdown.classList.toggle('dropdown-button-desocultar');
        }

        else if (el == buttonProva || el == buttonProvaI) {
            provaDropdown.classList.toggle('dropdown-button-desocultar');
        }

        else if (el == buttonBanca || el == buttonBancaI) {
            bancaDropdown.classList.toggle('dropdown-button-desocultar');
        }

        else if (el == buttonEstado || el == buttonEstadoI) {
            estadoDropdown.classList.toggle('dropdown-button-desocultar');
        }

        else if (el == acerteiQuestoesLabel1) {
            acerteiQuestoesLabel1.classList.add('selecionado');
            acerteiQuestoesLabel2.classList.remove('selecionado');
            acerteiQuestoesLabel3.classList.remove('selecionado');
            acerteiQuestoesLabel4.classList.remove('selecionado');
        }
        else if (el == acerteiQuestoesLabel2) {
            acerteiQuestoesLabel1.classList.remove('selecionado');
            acerteiQuestoesLabel2.classList.add('selecionado');
            acerteiQuestoesLabel3.classList.remove('selecionado');
            acerteiQuestoesLabel4.classList.remove('selecionado');
        }
        else if (el == acerteiQuestoesLabel3) {
            acerteiQuestoesLabel1.classList.remove('selecionado');
            acerteiQuestoesLabel2.classList.remove('selecionado');
            acerteiQuestoesLabel3.classList.add('selecionado');
            acerteiQuestoesLabel4.classList.remove('selecionado');
        }
        else if (el == acerteiQuestoesLabel4) {
            acerteiQuestoesLabel1.classList.remove('selecionado');
            acerteiQuestoesLabel2.classList.remove('selecionado');
            acerteiQuestoesLabel3.classList.remove('selecionado');
            acerteiQuestoesLabel4.classList.add('selecionado');
        }

        else if (el == filtroPalavraChaveI) {
            palavraChave.value = '';
            filtroPalavraChave.style.display = 'none';
        }

        else if (el.classList.contains('fa-circle-xmark')) {
            el.parentElement.remove();
            let textoSpan = el.nextElementSibling.nextElementSibling.innerText;

            for (let i = 0; i < disciplinaDropdownLabelSpan.length; i++) {
                if (disciplinaDropdownLabelSpan[i].innerText.trim() == textoSpan) {
                    disciplinaDropdownLabelSpan[i].previousElementSibling.checked = false;
                }
            }

            for (let i = 0; i < anoDropdownLabelSpan.length; i++) {
                if (anoDropdownLabelSpan[i].innerText.trim() == textoSpan) {
                    anoDropdownLabelSpan[i].previousElementSibling.checked = false;
                }
            }

            for (let i = 0; i < provaDropdownLabelSpan.length; i++) {
                if (provaDropdownLabelSpan[i].innerText.trim() == textoSpan) {
                    provaDropdownLabelSpan[i].previousElementSibling.checked = false;
                }
            }

            for (let i = 0; i < bancaDropdownLabelSpan.length; i++) {
                if (bancaDropdownLabelSpan[i].innerText.trim() == textoSpan) {
                    bancaDropdownLabelSpan[i].previousElementSibling.checked = false;
                }
            }

            for (let i = 0; i < estadoDropdownLabelSpan.length; i++) {
                if (estadoDropdownLabelSpan[i].innerText.trim() == textoSpan) {
                    estadoDropdownLabelSpan[i].previousElementSibling.checked = false;
                }
            }
            mensagemP();
        }

        // Respondendo Questão
        for(let y = 0; y < alternativas.length; y++){
            for(let x = 0; x < alternativas[y].children.length; x++){
                if (alternativas[y].children[x].children[0] == el){
                    alternativas[y].children[x].children[1].children[1].classList.toggle('cortado');
                    el.classList.toggle('cortado');
                    alternativas[y].children[x].children[1].children[0].classList.toggle('cortado');

                    alternativas[y].children[x].children[1].children[2].checked = false;
                    alternativas[y].children[x].children[1].children[0].classList.remove('selecionado');

                    let inputChecked = false;
                    for(let w = 0; w < alternativas[y].children.length; w++){
                        if(alternativas[y].children[x].children[1].children[2].checked){
                            inputChecked = true;
                        }
                    }
                    if(!inputChecked){
                        gabaritoInput[y].classList.add('desabilitado');
                    }
                    break;
                }
            }
        }

    });

    document.addEventListener('input', e => {

        const el = e.target;

        if (el == palavraChave) {

            if (palavraChave.value != '') {
                filtroPalavraChave.style.display = 'flex';
                filtroPalavraChaveSpan.innerHTML = palavraChave.value;

                filtrosSelecionadosP.style.display = 'none';
            } else {
                filtroPalavraChave.style.display = 'none';

                mensagemP();
            }
        }

        let validadorDisciplina = false;
        if (el == disciplinaDropdownInput) {
            for (let i = 0; i < disciplinaDropdownLabelSpan.length; i++) {
                let textoSpan = disciplinaDropdownLabelSpan[i].innerText.toLowerCase();
                let textoInput = disciplinaDropdownInput.value.toLowerCase();
                if (textoSpan.indexOf(textoInput) == -1) {
                    disciplinaDropdownLabel[i].style.display = 'none';
                } else {
                    disciplinaDropdownLabel[i].style.display = 'block';
                    validadorDisciplina = true;
                }
            }
            if (validadorDisciplina) {
                disciplinaDropdownH4.style.display = 'none';
            } else {
                disciplinaDropdownH4.style.display = 'block';
            }
        }

        let validadorAno = false;
        if (el == anoDropdownInput) {
            for (let i = 0; i < anoDropdownLabelSpan.length; i++) {
                let textoSpan = anoDropdownLabelSpan[i].innerText.toLowerCase();
                let textoInput = anoDropdownInput.value.toLowerCase();
                if (textoSpan.indexOf(textoInput) == -1) {
                    anoDropdownLabel[i].style.display = 'none';
                } else {
                    anoDropdownLabel[i].style.display = 'block';
                    validadorAno = true;
                }
            }
            if (validadorAno) {
                anoDropdownH4.style.display = 'none';
            } else {
                anoDropdownH4.style.display = 'block';
            }
        }

        let validadorProva = false;
        if (el == provaDropdownInput) {
            for (let i = 0; i < provaDropdownLabelSpan.length; i++) {
                let textoSpan = provaDropdownLabelSpan[i].innerText.toLowerCase();
                let textoInput = provaDropdownInput.value.toLowerCase();
                if (textoSpan.indexOf(textoInput) == -1) {
                    provaDropdownLabel[i].style.display = 'none';
                } else {
                    provaDropdownLabel[i].style.display = 'block';
                    validadorProva = true;
                }
            }
            if (validadorProva) {
                provaDropdownH4.style.display = 'none';
            } else {
                provaDropdownH4.style.display = 'block';
            }
        }

        let validadorBanca = false;
        if (el == bancaDropdownInput) {
            for (let i = 0; i < bancaDropdownLabelSpan.length; i++) {
                let textoSpan = bancaDropdownLabelSpan[i].innerText.toLowerCase();
                let textoInput = bancaDropdownInput.value.toLowerCase();
                if (textoSpan.indexOf(textoInput) == -1) {
                    bancaDropdownLabel[i].style.display = 'none';
                } else {
                    bancaDropdownLabel[i].style.display = 'block';
                    validadorBanca = true;
                }
            }
            if (validadorBanca) {
                bancaDropdownH4.style.display = 'none';
            } else {
                bancaDropdownH4.style.display = 'block';
            }
        }

        let validadorEstado = false;
        if (el == estadoDropdownInput) {
            for (let i = 0; i < estadoDropdownLabelSpan.length; i++) {
                let textoSpan = estadoDropdownLabelSpan[i].innerText.toLowerCase();
                let textoInput = estadoDropdownInput.value.toLowerCase();
                if (textoSpan.indexOf(textoInput) == -1) {
                    estadoDropdownLabel[i].style.display = 'none';
                } else {
                    estadoDropdownLabel[i].style.display = 'block';
                    validadorEstado = true;
                }
            }
            if (validadorEstado) {
                estadoDropdownH4.style.display = 'none';
            } else {
                estadoDropdownH4.style.display = 'block';
            }
        }

    });

    function createDivFiltrosSelecionados(text, word, classe) {
        const div = document.createElement('div');
        div.classList.add(classe);
        div.style.display = 'flex';

        const i = document.createElement('i');
        i.classList.add('fa-regular');
        i.classList.add('fa-circle-xmark');

        const p = document.createElement('p');
        p.innerHTML = word;

        const span = document.createElement('span');
        span.innerHTML = text;

        div.appendChild(i);
        div.appendChild(p);
        div.appendChild(span);

        return div;
    }

    document.addEventListener('change', e => {

        const el = e.target;

        for (let i = 0; i < disciplinaDropdownLabelInput.length; i++) {
            if (el == disciplinaDropdownLabelInput[i] && disciplinaDropdownLabelInput[i].checked) {
                let textoLabelSpan = disciplinaDropdownLabelSpan[i].innerText;
                const div = createDivFiltrosSelecionados(textoLabelSpan, 'Disciplina', 'filtro_disciplina');
                filtrosSelecionados.appendChild(div);
                break;
            } else if (el == disciplinaDropdownLabelInput[i] && !disciplinaDropdownLabelInput[i].checked) {
                let textoLabelSpan = disciplinaDropdownLabelSpan[i].innerText;
                let validador = false;
                for (let x = 0; x < filtrosSelecionados.children.length; x++) {

                    if (filtrosSelecionados.children[x].classList.contains('filtro_disciplina')) {
                        if (filtrosSelecionados.children[x].firstElementChild.nextElementSibling.nextElementSibling.innerText == textoLabelSpan) {
                            filtrosSelecionados.children[x].remove();
                            validador = true;
                            break;
                        }
                    }

                }
                if (validador) {
                    break;
                }
            }

        }

        for (let i = 0; i < anoDropdownLabelInput.length; i++) {
            if (el == anoDropdownLabelInput[i] && anoDropdownLabelInput[i].checked) {
                let textoLabelSpan = anoDropdownLabelSpan[i].innerText;
                const div = createDivFiltrosSelecionados(textoLabelSpan, 'Ano', 'filtro_ano');
                filtrosSelecionados.appendChild(div);
                break;
            } else if (el == anoDropdownLabelInput[i] && !anoDropdownLabelInput[i].checked) {
                let textoLabelSpan = anoDropdownLabelSpan[i].innerText;
                let validador = false;
                for (let x = 0; x < filtrosSelecionados.children.length; x++) {

                    if (filtrosSelecionados.children[x].classList.contains('filtro_ano')) {
                        if (filtrosSelecionados.children[x].firstElementChild.nextElementSibling.nextElementSibling.innerText == textoLabelSpan) {
                            filtrosSelecionados.children[x].remove();
                            validador = true;
                            break;
                        }
                    }

                }
                if (validador) {
                    break;
                }
            }

        }

        for (let i = 0; i < provaDropdownLabelInput.length; i++) {
            if (el == provaDropdownLabelInput[i] && provaDropdownLabelInput[i].checked) {
                let textoLabelSpan = provaDropdownLabelSpan[i].innerText;
                const div = createDivFiltrosSelecionados(textoLabelSpan, 'Prova', 'filtro_prova');
                filtrosSelecionados.appendChild(div);
                break;
            } else if (el == provaDropdownLabelInput[i] && !provaDropdownLabelInput[i].checked) {
                let textoLabelSpan = provaDropdownLabelSpan[i].innerText;
                let validador = false;
                for (let x = 0; x < filtrosSelecionados.children.length; x++) {

                    if (filtrosSelecionados.children[x].classList.contains('filtro_prova')) {
                        if (filtrosSelecionados.children[x].firstElementChild.nextElementSibling.nextElementSibling.innerText == textoLabelSpan) {
                            filtrosSelecionados.children[x].remove();
                            validador = true;
                            break;
                        }
                    }

                }
                if (validador) {
                    break;
                }
            }

        }

        for (let i = 0; i < bancaDropdownLabelInput.length; i++) {
            if (el == bancaDropdownLabelInput[i] && bancaDropdownLabelInput[i].checked) {
                let textoLabelSpan = bancaDropdownLabelSpan[i].innerText;
                const div = createDivFiltrosSelecionados(textoLabelSpan, 'Banca', 'filtro_banca');
                filtrosSelecionados.appendChild(div);
                break;
            } else if (el == bancaDropdownLabelInput[i] && !bancaDropdownLabelInput[i].checked) {
                let textoLabelSpan = bancaDropdownLabelSpan[i].innerText;
                let validador = false;
                for (let x = 0; x < filtrosSelecionados.children.length; x++) {

                    if (filtrosSelecionados.children[x].classList.contains('filtro_banca')) {
                        if (filtrosSelecionados.children[x].firstElementChild.nextElementSibling.nextElementSibling.innerText == textoLabelSpan) {
                            filtrosSelecionados.children[x].remove();
                            validador = true;
                            break;
                        }
                    }

                }
                if (validador) {
                    break;
                }
            }

        }

        for (let i = 0; i < estadoDropdownLabelInput.length; i++) {
            if (el == estadoDropdownLabelInput[i] && estadoDropdownLabelInput[i].checked) {
                let textoLabelSpan = estadoDropdownLabelSpan[i].innerText;
                const div = createDivFiltrosSelecionados(textoLabelSpan, 'Estado', 'filtro_estado');
                filtrosSelecionados.appendChild(div);
                break;
            } else if (el == estadoDropdownLabelInput[i] && !estadoDropdownLabelInput[i].checked) {
                let textoLabelSpan = estadoDropdownLabelSpan[i].innerText;
                let validador = false;
                for (let x = 0; x < filtrosSelecionados.children.length; x++) {

                    if (filtrosSelecionados.children[x].classList.contains('filtro_estado')) {
                        if (filtrosSelecionados.children[x].firstElementChild.nextElementSibling.nextElementSibling.innerText == textoLabelSpan) {
                            filtrosSelecionados.children[x].remove();
                            validador = true;
                            break;
                        }
                    }

                }
                if (validador) {
                    break;
                }
            }

        }

        mensagemP();

        // Respondendo Questão
        for(let y = 0; y < alternativas.length; y++){
            let validadorAlternativaMarcada = false;
            for(let x = 0; x < alternativas[y].children.length; x++){
                if(alternativas[y].children[x].children[1].children[2].checked){
                    alternativas[y].children[x].children[1].children[0].classList.add('selecionado');
                    alternativas[y].children[x].children[1].children[1].classList.remove('cortado');
                    alternativas[y].children[x].children[0].classList.remove('cortado');
                    alternativas[y].children[x].children[1].children[0].classList.remove('cortado');
                    validadorAlternativaMarcada = true;
                } else{
                    alternativas[y].children[x].children[1].children[0].classList.remove('selecionado');
                }
            }

            if(validadorAlternativaMarcada){
                gabaritoInput[y].classList.remove('desabilitado');
            } else{
                gabaritoInput[y].classList.add('desabilitado');
            }
        }


    });

})();