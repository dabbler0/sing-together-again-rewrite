import encoding from '@/encoding'

function formatQs (data) {
  const components = []
  for (const key in data) {
    components.push(key + '=' +
      encodeURIComponent(data[key]))
  }

  return '?' + components.join('&')
}
function get (url, data, retry) {
  const q = new XMLHttpRequest()
  q.open('GET', url +
    formatQs(data), true)

  q.responseType = 'arraybuffer'

  return new Promise((resolve, reject) => {
    function rejectOrRetry (error) {
      if (retry) {
        setTimeout(() => {
          resolve(get(url, data, retry))
        }, 500)
      } else {
        reject(error)
      }
    }

    q.addEventListener('load', () => {
      if (q.status === 200) {
        try {
          resolve(encoding.decode(
            new Uint8Array(q.response)))
        } catch (e) {
          rejectOrRetry(new Error('Invalid server response ' + e.toString()))
        }
      } else {
        rejectOrRetry(new Error('Server response status was ' + q.status))
      }
    })

    q.addEventListener('error', rejectOrRetry)
    q.addEventListener('abort', rejectOrRetry)

    q.send()
  })
}

function post (url, qsData, postData, retry) {
  const q = new XMLHttpRequest()
  q.open('POST', url +
    formatQs(qsData), true)

  q.responseType = 'arraybuffer'

  return new Promise((resolve, reject) => {
    function rejectOrRetry (error) {
      if (retry) {
        setTimeout(() => {
          resolve(post(url, qsData, postData, retry))
        }, 500)
      } else {
        reject(error)
      }
    }

    q.addEventListener('load', () => {
      if (q.status === 200) {
        try {
          resolve(encoding.decode(
            new Uint8Array(q.response)))
        } catch (e) {
          rejectOrRetry(new Error('Invalid server response'))
        }
      } else {
        rejectOrRetry(new Error('Server response status was ' + q.status))
      }
    })
    q.addEventListener('error', rejectOrRetry)
    q.addEventListener('abort', rejectOrRetry)
    q.send(new Blob([encoding.encode(postData).buffer]))
  })
}

export default {get, post}
