document.addEventListener("DOMContentLoaded", () => {
    const elementoRelogio = document.getElementById("clock");
    const tempoInicialEmSegundos = 120; 
    let tempoRestante;

    // Função para formatar os componentes de tempo
    const formatarComponenteDeTempo = (tempo) => (tempo < 10 ? "0" + tempo : tempo);

    // Atualiza o display do relógio
    const atualizarRelogio = () => {
        const horas = Math.floor(tempoRestante / 3600);
        const minutos = Math.floor((tempoRestante % 3600) / 60);
        const segundos = tempoRestante % 60;

        elementoRelogio.textContent = `${formatarComponenteDeTempo(horas)}:${formatarComponenteDeTempo(minutos)}:${formatarComponenteDeTempo(segundos)}`;
    };

    // Lê o tempo restante do localStorage ou inicializa
    const inicializarTempoRestante = () => {
        const tempoRestanteArmazenado = localStorage.getItem("remainingTime");
        tempoRestante = tempoRestanteArmazenado ? parseInt(tempoRestanteArmazenado) : tempoInicialEmSegundos;

        if (!tempoRestanteArmazenado) {
            localStorage.setItem("remainingTime", tempoRestante.toString());
        }
    };

    // Função principal do contador
    const atualizarContagemRegressiva = () => {
        if (tempoRestante <= 0) {
            elementoRelogio.textContent = "Tempo expirado";
            localStorage.removeItem("remainingTime");
            return;
        }

        atualizarRelogio();
        tempoRestante--;
        localStorage.setItem("remainingTime", tempoRestante.toString());

        setTimeout(atualizarContagemRegressiva, 1000);
    };

    // Reiniciar o valor da sessão ao atualizar a página
    window.addEventListener("beforeunload", () => {
        localStorage.removeItem("remainingTime");
    });

    // Inicializa o temporizador e começa a contagem
    inicializarTempoRestante();
    atualizarContagemRegressiva();
});