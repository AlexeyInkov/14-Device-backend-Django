let CSRF_TOKEN = '{{ csrf_token }}';
document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = CSRF_TOKEN;
})

// // https://blog.benoitblanchon.fr/django-htmx-modal-form/
//
// const verificationsModal = new bootstrap.Modal(document.getElementById("verificationsModal"))
// const loadFileModal = new bootstrap.Modal(document.getElementById("loadFileModal"))
// console.log(verificationsModal)
// console.log(loadFileModal)
// htmx.on("htmx:afterSwap", (e) => {
//   console.log(e.detail)
//   // Response targeting #dialog => show the modal
//   if (e.detail.target.id == "dialogVerifications") {
//     verificationsModal.show()
//   }
//   if (e.detail.target.id == "dialogLoadFile") {
//       loadFileModal.show()
//     }
// })
//
// htmx.on("htmx:beforeSwap", (e) => {
//   // Empty response targeting #dialog => hide the modal
//   if (e.detail.target.id == "dialogVerifications" && !e.detail.xhr.response) {
//     verificationsModal.hide()
//     e.detail.shouldSwap = false
//   }
//   if (e.detail.target.id == "dialogLoadFile" && !e.detail.xhr.response) {
//     loadFileModal.hide()
//     e.detail.shouldSwap = false
//   }
// })


