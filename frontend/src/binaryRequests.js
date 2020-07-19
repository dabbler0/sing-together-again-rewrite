import encoding from '@/encoding'

function formatQs (data) {
  const components = []
  for (const key in data) {
    components.push(key + '=' +
      encodeURIComponent(data[key]))
  }

  return '?' + components.join('&')
}
function get (url, data) {
  const q = new XMLHttpRequest()
  q.open('GET', url +
    formatQs(data), true)

  q.responseType = 'arraybuffer'

  return new Promise((resolve, reject) => {
    q.addEventListener('load', () => {
      resolve(encoding.decode(
        new Uint8Array(q.response)))
    })

    q.addEventListener('error', reject)

    q.send()
  })
}

function post (url, qsData, postData) {
  const q = new XMLHttpRequest()
  q.open('POST', url +
    formatQs(qsData), true)

  q.responseType = 'arraybuffer'

  return new Promise((resolve, reject) => {
    q.addEventListener('load', () => {
      resolve(encoding.decode(
        new Uint8Array(q.response)))
    })
    q.addEventListener('error', reject)
    q.send(new Blob([encoding.encode(postData).buffer]))
  })
}

export default {get, post}
