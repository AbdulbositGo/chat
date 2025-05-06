document.addEventListener('keydown', function (event) {
    if ((event.ctrlKey || event.metaKey) && (event.key === '+' || event.key === '-')) {
        event.preventDefault()
    }
})
function getOfflineStatus() {
    const offlineBox = document.getElementById('offline-budge')
    if (!navigator.onLine) {
        offlineBox.classList.remove('hidden')
    }
}
function getOnlineStatus() {
    const onlineBox = document.getElementById('online-budge')
    const offlineBox = document.getElementById('offline-budge')

    offlineBox.classList.add('hidden')
    onlineBox.classList.remove('hidden')
    setTimeout(() => {
        onlineBox.classList.add('hidden')
    }, 2500)
}

window.addEventListener('offline', getOfflineStatus)
window.addEventListener('online', getOnlineStatus)