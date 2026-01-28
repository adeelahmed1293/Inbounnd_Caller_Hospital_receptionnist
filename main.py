from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os



load_dotenv()

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
API_KEY = os.getenv("TWILIO_API_KEY")
API_SECRET = os.getenv("TWILIO_API_SECRET")
TWIML_APP_SID = os.getenv("TWILIO_TWIML_APP_SID")
PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
SIP_HOST = os.getenv("LIVEKIT_SIP_HOST")
SIP_USER = os.getenv("LIVEKIT_SIP_USERNAME")
SIP_PASS = os.getenv("LIVEKIT_SIP_PASSWORD")


@app.get("/token")
def token():
    """Generate Twilio access token for browser WebRTC"""
    token = AccessToken(
        ACCOUNT_SID,
        API_KEY,
        API_SECRET,
        identity="browser-user"
    )

    grant = VoiceGrant(
        outgoing_application_sid=TWIML_APP_SID,
        incoming_allow=True
    )

    token.add_grant(grant)
    return {"token": token.to_jwt()}


@app.post("/voice")
async def voice(request: Request):
    """Twilio webhook - forwards call to LiveKit SIP"""
    print("📞 Incoming call received - routing to LiveKit SIP")
    
    response = VoiceResponse()
    # Use callerId to set a valid E.164 phone number for SIP
    dial = response.dial(caller_id=PHONE_NUMBER)
    dial.sip(
        f"sip:{PHONE_NUMBER}@{SIP_HOST}",
        username=SIP_USER,
        password=SIP_PASS
    )
    
    print(f"🔊 TwiML Response:\n{str(response)}")
    return HTMLResponse(str(response), media_type="application/xml")


@app.get("/", response_class=HTMLResponse)
def index():
    """Browser interface for making calls"""
    html = """
<!DOCTYPE html>
<html>
<head>
  <title>Twilio Browser → LiveKit Test</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 600px;
      margin: 50px auto;
      padding: 20px;
      text-align: center;
    }
    button {
      padding: 15px 30px;
      font-size: 16px;
      margin: 10px;
      cursor: pointer;
      border-radius: 5px;
      border: none;
    }
    #callBtn {
      background-color: #4CAF50;
      color: white;
    }
    #hangupBtn {
      background-color: #f44336;
      color: white;
    }
    #status {
      margin-top: 20px;
      padding: 15px;
      border-radius: 5px;
      font-weight: bold;
    }
    .idle { background-color: #f0f0f0; }
    .loading { background-color: #fff3cd; }
    .calling { background-color: #d1ecf1; }
    .connected { background-color: #d4edda; }
    .error { background-color: #f8d7da; }
  </style>
</head>
<body>
  <h2>🎙️ Twilio Browser → LiveKit SIP Test</h2>
  <p>Call your Twilio number from the browser (no phone needed)</p>
  
  <button id="callBtn" onclick="startCall()">📞 Call My Twilio Number</button>
  <button id="hangupBtn" onclick="hangup()" disabled>❌ Hang Up</button>
  
  <div id="status" class="idle">Status: Idle</div>
  <div id="logs" style="margin-top: 20px; text-align: left; font-family: monospace; font-size: 12px;"></div>

  <script src="/static/twilio.min.js"></script>
  
  <script>
    let device;
    let activeCall;
    
    function log(message) {
      const logs = document.getElementById("logs");
      const timestamp = new Date().toLocaleTimeString();
      logs.innerHTML += "[" + timestamp + "] " + message + "<br>";
      logs.scrollTop = logs.scrollHeight;
      console.log(message);
    }
    
    function updateStatus(text, className) {
      const status = document.getElementById("status");
      status.innerText = "Status: " + text;
      status.className = className;
    }

    async function startCall() {
      try {
        document.getElementById("callBtn").disabled = true;
        updateStatus("Getting token...", "loading");
        log("🔑 Requesting access token...");

        // Check if Twilio is loaded
        if (typeof Twilio === 'undefined' || typeof Twilio.Device === 'undefined') {
          throw new Error("Twilio SDK not loaded. Check /static/twilio.min.js");
        }

        const res = await fetch("/token");
        if (!res.ok) {
          throw new Error("Token request failed: " + res.status);
        }
        
        const data = await res.json();
        log("✅ Token received");
        
        updateStatus("Initializing device...", "loading");
        log("🔧 Initializing Twilio Device (v2.x)...");
        
        // Initialize Twilio Device v2.x
        device = new Twilio.Device(data.token, {
          logLevel: 1,
          codecPreferences: ['opus', 'pcmu'],
          sounds: {
            incoming: false,
            outgoing: false,
            disconnect: false
          }
        });

        // Device registered and ready
        device.on('registered', function() {
          log("✅ Device registered");
          updateStatus("Calling...", "calling");
          log("📞 Placing call to """ + PHONE_NUMBER + """");
          document.getElementById("hangupBtn").disabled = false;
          
          // Make the call
          var params = {
            To: '""" + PHONE_NUMBER + """'
          };
          
          activeCall = device.connect({ params: params });
          
          // Setup call event handlers
          setupCallHandlers(activeCall);
        });

        // Device error
        device.on('error', function(error) {
          updateStatus("Device Error: " + error.message, "error");
          log("❌ Device Error: " + error.message);
          console.error('Twilio Device Error:', error);
          document.getElementById("callBtn").disabled = false;
          document.getElementById("hangupBtn").disabled = true;
        });

        // Register the device
        device.register();
        
      } catch (error) {
        updateStatus("Error: " + error.message, "error");
        log("❌ Exception: " + error.message);
        console.error(error);
        document.getElementById("callBtn").disabled = false;
      }
    }

    function setupCallHandlers(call) {
      call.on('accept', function() {
        updateStatus("Connected ✓", "connected");
        log("✅ Call connected!");
      });

      call.on('disconnect', function() {
        updateStatus("Disconnected", "idle");
        log("📴 Call ended");
        document.getElementById("callBtn").disabled = false;
        document.getElementById("hangupBtn").disabled = true;
        activeCall = null;
      });

      call.on('cancel', function() {
        updateStatus("Call cancelled", "idle");
        log("📴 Call cancelled");
        document.getElementById("callBtn").disabled = false;
        document.getElementById("hangupBtn").disabled = true;
        activeCall = null;
      });

      call.on('error', function(error) {
        updateStatus("Call Error: " + error.message, "error");
        log("❌ Call Error: " + error.message);
        console.error('Call Error:', error);
        document.getElementById("callBtn").disabled = false;
        document.getElementById("hangupBtn").disabled = true;
      });

      call.on('reject', function() {
        updateStatus("Call rejected", "error");
        log("❌ Call rejected");
        document.getElementById("callBtn").disabled = false;
        document.getElementById("hangupBtn").disabled = true;
      });
    }

    function hangup() {
      log("📴 Hanging up...");
      
      if (activeCall) {
        activeCall.disconnect();
      }
      
      if (device) {
        device.disconnectAll();
      }
      
      updateStatus("Disconnected", "idle");
      document.getElementById("callBtn").disabled = false;
      document.getElementById("hangupBtn").disabled = true;
      activeCall = null;
    }

    // Log when page loads
    window.addEventListener('DOMContentLoaded', function() {
      if (typeof Twilio !== 'undefined' && typeof Twilio.Device !== 'undefined') {
        log("✅ Twilio Voice SDK v2.x loaded successfully");
      } else {
        log("❌ Twilio SDK failed to load - please check console");
        updateStatus("Error: Twilio SDK not loaded", "error");
      }
    });
  </script>
</body>
</html>
"""
    return html


