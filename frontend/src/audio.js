let mediaStream = null

function getMediaStream () {
  if (mediaStream != null) {
    return Promise.resolve(mediaStream)
  } else {
    return navigator.mediaDevices.getUserMedia(
      {audio: true, video: false}
    ).then((stream) => {
      mediaStream = stream
      return stream
    })
  }
}

function recordMedia (stream) {
  stream = stream.clone()

  const mediaRecorder = new MediaRecorder(stream, {mimeType: 'audio/webm'})

  const data = []

  mediaRecorder.addEventListener('dataavailable', (e) => {
    if (e.data.size > 0) {
      data.push(e.data)
    }
  })

  mediaRecorder.start()

  return {
    stop: () => mediaRecorder.stop(),
    data: new Promise((resolve, reject) => {
      mediaRecorder.addEventListener('stop', (e) => {
        // For the time begin we are only allowing recording
        // in a single chunk. TODO change?
        resolve(new Response(data[0]).arrayBuffer())
      })
    })
  }
}

function playAudioBuffer (context, buffer, time) {
  const bufferSource = context.createBufferSource()
  bufferSource.buffer = buffer
  bufferSource.connect(context.destination)

  if (time < context.currentTime) {
    bufferSource.start(0, context.currentTime - time)
  } else {
    bufferSource.start(time)
  }
}

function createOscillatorBuffer (context, duration) {
  const buffer = context.createBuffer(2, context.sampleRate * duration, context.sampleRate)

  for (let channel = 0; channel < buffer.numberOfChannels; channel++) {
    const currentChannel = buffer.getChannelData(channel)
    for (let i = 0; i < buffer.length; i++) {
      currentChannel[i] = Math.sin(2 * Math.PI * i * 440 / context.sampleRate)
    }
  }

  return buffer
}

function recordAtTime (context, stream, startTime, endTime) {
  return new Promise((resolve, reject) => {
    function timeCheck () {
      if (startTime - context.currentTime < 0.5) {
        beginRecording()
      } else {
        setTimeout(timeCheck, 100)
      }
    }

    function beginRecording () {
      const recorder = recordMedia(stream)

      console.log('Wanted to start recording at', startTime, 'and it is', context.currentTime)

      resolve(Promise.all([recorder.data, startTime - context.currentTime]))

      setTimeout(
        recorder.stop,
        (endTime - context.currentTime) * 1000 + 100
      )
    }

    timeCheck()
  })
}

function measureLatency (context) {
  const supposedTime = context.currentTime + 1
  const buffer = createOscillatorBuffer(context, 0.5)

  return getMediaStream().then((stream) => {
    // Play and record simultaneously
    playAudioBuffer(context, buffer, supposedTime)
    return recordAtTime(context, stream, supposedTime, supposedTime + 1)
  }).then(([buffer, offset]) => {
    // Decode the resulting audio
    return Promise.all([context.decodeAudioData(buffer), offset])
  }).then(([audioBuffer, offset]) => {
    // Determine when the audio was first heard
    const channelData = audioBuffer.getChannelData(0)

    const maximum = Math.max.apply(window, channelData)
    const minimum = Math.min.apply(window, channelData)

    let thresh = Math.min(Math.abs(maximum) / 2,
      Math.abs(minimum) / 2)

    const startIndex = Math.round(audioBuffer.sampleRate * offset)
    const endIndex = startIndex + audioBuffer.sampleRate * 1

    while (true) {
      for (let i = startIndex; i < endIndex; i++) {
        if (Math.abs(channelData[i]) > thresh) {
          return (i - startIndex) / audioBuffer.sampleRate
        }
      }
      thresh /= 2
    }
  })
}

export default {
  getMediaStream,
  recordMedia,
  playAudioBuffer,
  createOscillatorBuffer,
  recordAtTime,
  measureLatency
}
