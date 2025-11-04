const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function appendUser(msg){
  const d = document.createElement("div");
  d.className = "message msg-user";
  d.innerText = msg;
  chatBox.appendChild(d);
}
function appendBot(msg){
  const d = document.createElement("div");
  d.className = "message msg-bot";
  d.innerText = msg;
  chatBox.appendChild(d);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(){
  const text = input.value.trim();
  if(!text) return;
  appendUser(text);
  input.value = "";
  appendBot("Thinking...");
  try{
    const res = await fetch("/chat", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message: text})
    });
    const data = await res.json();
    // Replace last bot placeholder with real reply
    const bots = document.querySelectorAll(".msg-bot");
    bots[bots.length - 1].innerText = data.reply;
  }catch(e){
    const bots = document.querySelectorAll(".msg-bot");
    bots[bots.length - 1].innerText = "Sorry — something went wrong. Try again.";
  }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e)=> { if(e.key === "Enter") sendMessage(); });
