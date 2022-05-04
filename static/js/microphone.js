if ("webkitSpeechRecognition" in window) {
  let speechRecognition = new webkitSpeechRecognition();
  let final_transcript = "";

  speechRecognition.continuous = true;
  speechRecognition.interimResults = true;
  speechRecognition.lang = "English";

  speechRecognition.onstart = () => {
    document.querySelector("#dstatus").style.display = "block";
  };
  speechRecognition.onerror = () => {
    document.querySelector("#dstatus").style.display = "none";
    console.log("Speech Recognition Error");
  };
  speechRecognition.onend = () => {
    document.querySelector("#dstatus").style.display = "none";
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
    console.log(interim_transcript);
    console.log(final_transcript);
    document.querySelector("#final").innerHTML = final_transcript;
    document.querySelector("#interim").innerHTML = interim_transcript;
  };

  document.querySelector("#start").onclick = () => {
    speechRecognition.start();
  };

  document.querySelector("#submit").onclick = async () => {
    let diag = document.querySelector("#final").innerHTML;
    // let dos = document.querySelector("#dfinal").innerHTML;
    // let advice = document.querySelector("#afinal").innerHTML;
    const requestOptions = {
      method: "POST",
      // body: JSON.stringify([diag, dos, advice]),
      body: JSON.stringify([diag]),
    };
    await fetch("/voicepres/", requestOptions);
    location.href = `/verify${generateQueryString()}`;
  };

  document.querySelector("#stop").onclick = () => {
    speechRecognition.stop();
  };

  document.querySelector("#clear").onclick = () => {
    speechRecognition.stop();
    final_transcript = "";
  };
} else {
  console.log("Speech Recognition Not Available");
}
