if ("webkitSpeechRecognition" in window) {
  let speechRecognition = new webkitSpeechRecognition();
  let final_transcript = "";

  speechRecognition.continuous = true;
  speechRecognition.interimResults = true;
  speechRecognition.lang = "English";

  speechRecognition.onstart = () => {
    document.querySelector("#astatus").style.display = "block";
  };
  speechRecognition.onerror = () => {
    document.querySelector("#astatus").style.display = "none";
    console.log("Speech Recognition Error");
  };
  speechRecognition.onend = () => {
    document.querySelector("#astatus").style.display = "none";
    console.log("Speech Recognition Ended");
  };

  speechRecognition.onresult = (event) => {
    let interim_transcript = "";

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    document.querySelector("#afinal").innerHTML = final_transcript;
    document.querySelector("#ainterim").innerHTML = interim_transcript;
    final_transcript = "";
    interim_transcript = "";
  };

  document.querySelector("#astart").onclick = () => {
    speechRecognition.start();
  };

  document.querySelector("#submit").onclick = () => {
    let ft = document.querySelector("#afinal").innerHTML;
    const requestOptions = {
      method: "POST",
      body: ft,
    };
    fetch("/voicepres/", requestOptions);
  };

  document.querySelector("#astop").onclick = () => {
    speechRecognition.stop();
  };
} else {
  console.log("Speech Recognition Not Available");
}
