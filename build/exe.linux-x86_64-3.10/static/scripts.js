function carregarUsuarios() {
    $("#bem-vindo").hide();

    // Fazer uma nova solicitação ao servidor para obter dados atualizados
    $.get("/recarregar_usuarios", function (data) {
        var listaUsuarios = "<ul>";
        data.forEach(function (user) {
            listaUsuarios += "<li><button onclick='confirmarExclusao(\"" + user.name +  "\")'>" + user.name + ' '+ user.password +  ' '+ user.status + "</button></li>";
        });
        listaUsuarios += "</ul>";

        $("#lista-usuarios").html(listaUsuarios);
    });
}

// Função para confirmar exclusão do usuário
function confirmarExclusao(username,password) {
    var confirmacao = confirm("Você quer excluir o usuário " + username + "?");

    if (confirmacao) {
        $.post("/excluir_usuario", { username: username }, function (response) {
            // Atualize a lista de usuários após a exclusão
            carregarUsuarios();
        });
    } else {
        console.log("Exclusão cancelada");
    }
}



$("#bem-vindo").hide();

// Fazer uma nova solicitação ao servidor para obter dados atualizados
$.get("/recarregar_usuarios", function (data) {
    var listaUsuarios = "<ul>";
    data.forEach(function (user) {
        
    });

   
});
