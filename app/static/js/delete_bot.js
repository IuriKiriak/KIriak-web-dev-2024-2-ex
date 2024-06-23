let deleteUserModal = document.querySelector('#deleteBot')

deleteUserModal.addEventListener('show.bs.modal', function(event){
    let form = document.querySelector('.modal-form')
    form.action = event.relatedTarget.dataset.action;
    let userLogin = deleteUserModal.querySelector('.name-bot');
    //userLogin.textContent = event.relatedTarget.closest('tr').querySelector('.user-login').textContent;
});