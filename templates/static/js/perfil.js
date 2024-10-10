(function () {
    const filtrosSelecionados = document.querySelector('.filtros_selecionados');
    const filtrosSelecionadosP = document.querySelector('.filtros_selecionados>p');

    const buttonDisciplina = document.querySelector('.button-disciplina');
    const buttonDisciplinaI = document.querySelector('.button-disciplina i');
    const disciplinaDropdown = document.querySelector('.button-disciplina .dropdown-button');
    const disciplinaDropdownInput = document.querySelector('.button-disciplina .dropdown-button>input');
    const disciplinaDropdownLabelSpan = document.querySelectorAll('.button-disciplina .dropdown-button label span');
    const disciplinaDropdownLabel = document.querySelectorAll('.button-disciplina .dropdown-button label');
    const disciplinaDropdownLabelInput = document.querySelectorAll('.button-disciplina .dropdown-button label input');
    const disciplinaDropdownH4 = document.querySelector('.button-disciplina .dropdown-button h4');

    function mensagemP() {
        let disciplinaChecked = false;
        for (let i = 0; i < disciplinaDropdownLabelInput.length; i++) {
            if (disciplinaDropdownLabelInput[i].checked) {
                disciplinaChecked = true;
                break;
            }
        }

        if (!disciplinaChecked) {
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

        else if (el.classList.contains('fa-circle-xmark')) {
            el.parentElement.remove();
            let textoSpan = el.nextElementSibling.nextElementSibling.innerText;

            for (let i = 0; i < disciplinaDropdownLabelSpan.length; i++) {
                if (disciplinaDropdownLabelSpan[i].innerText.trim() == textoSpan) {
                    disciplinaDropdownLabelSpan[i].previousElementSibling.checked = false;
                }
            }
            mensagemP();
        }

    });

    document.addEventListener('input', e => {

        const el = e.target;

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

                for (let x = 0; x < filtrosSelecionados.children.length; x++) {
                    if (filtrosSelecionados.children[x].classList.contains('filtro_disciplina')) {
                        filtrosSelecionados.children[x].remove();
                        break;
                    }
                }

                let textoLabelSpan = disciplinaDropdownLabelSpan[i].innerText;
                const div = createDivFiltrosSelecionados(textoLabelSpan, 'Disciplina', 'filtro_disciplina');
                filtrosSelecionados.appendChild(div);
                break;
            } 
        }

        mensagemP();

    });

})();