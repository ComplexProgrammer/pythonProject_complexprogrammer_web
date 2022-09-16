function addLocalVideo() {
  var track = Twilio.Video.createLocalVideoTrack();
  var video = document.getElementById('local').firstElementChild;
  console.log(track)
  console.log(video)
  video.appendChild(track.attach());
};

addLocalVideo();

const connect = async (username) => {
  const response = await fetch('/join_room', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({'username': username}),
  });
  const data = await response.json();
  room = await Twilio.Video.connect(data.token);
  room.participants.forEach(participantConnected);
  room.on('participantConnected', participantConnected);
  room.on('participantDisconnected', participantDisconnected);
  connected = true;
  updateParticipantCount();
};

const updateParticipantCount = () => {
  if (!connected) {
    count.innerHTML = 'Disconnected.';
  }
  else {
    count.innerHTML = (room.participants.size + 1) + ' participants online.';
  }
};

const participantConnected = (participant) => {
  const participantDiv = document.createElement('div');
  participantDiv.setAttribute('id', participant.sid);
  participantDiv.setAttribute('class', 'participant');

  const tracksDiv = document.createElement('div');
  participantDiv.appendChild(tracksDiv);

  const labelDiv = document.createElement('div');
  labelDiv.innerHTML = participant.identity;
  participantDiv.appendChild(labelDiv);

  container.appendChild(participantDiv);

  participant.tracks.forEach(publication => {
    if (publication.isSubscribed) {
      trackSubscribed(tracksDiv, publication.track);
    }
  });
  participant.on('trackSubscribed', track => trackSubscribed(tracksDiv, track));
  participant.on('trackUnsubscribed', trackUnsubscribed);
  updateParticipantCount();
};

const participantDisconnected = (participant) => {
  document.getElementById(participant.sid).remove();
  updateParticipantCount();
};

const trackSubscribed = (div, track) => {
  div.appendChild(track.attach());
};

const trackUnsubscribed = (track) => {
  track.detach().forEach(element => element.remove());
};

const disconnect = () => {
  room.disconnect();
  while (container.lastChild.id != 'local') {
      container.removeChild(container.lastChild);
  }
  button.innerHTML = 'Join call';
  connected = false;
  updateParticipantCount();
};

