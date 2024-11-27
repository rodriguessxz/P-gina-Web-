// Adicionar interatividade simples, como efeito de clique nas linhas da tabela
document.querySelectorAll('tr').forEach(row => {
    row.addEventListener('click', () => {
        row.style.backgroundColor = '#d4edda'; // cor de destaque
        setTimeout(() => {
            row.style.backgroundColor = ''; // resetar a cor após um tempo
        }, 300);
    });
});
