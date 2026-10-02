const API = "http://127.0.0.1:8000";
const token = () => localStorage.getItem("cc_token");

function authHeaders(json=false){
  const h = {};
  if(json) h["Content-Type"]="application/json";
  if(token()) h["Authorization"]=`Bearer ${token()}`;
  return h;
}
async function api(path, options={}){
  const res=await fetch(`${API}${path}`, options);
  let data=null; try{data=await res.json()}catch{}
  if(!res.ok) throw new Error(data?.detail || "Request failed");
  return data;
}
function saveSession(data, me){
  localStorage.setItem("cc_token", data.access_token);
  localStorage.setItem("cc_role", me.role);
  localStorage.setItem("cc_name", me.name);
}
function logout(){localStorage.clear(); location.href="index.html";}
function requireRole(role){
  if(!token() || localStorage.getItem("cc_role")!==role){
    location.href="login.html"; return false;
  }
  return true;
}
function esc(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));}
function fmtDate(v){return v?new Date(v).toLocaleDateString():"-";}
function tags(s){return (s||"").split(",").map(x=>x.trim()).filter(Boolean).map(x=>`<span class="tag">${esc(x)}</span>`).join("");}
function openNotifications(){
  const panel=document.getElementById("notifications");
  if(!panel)return;
  panel.classList.toggle("hidden");
  if(!panel.classList.contains("hidden")) loadNotifications();
}
async function loadNotifications(){
  const box=document.getElementById("notifications");
  if(!box)return;
  try{
    const items=await api("/applications/notifications",{headers:authHeaders()});
    box.innerHTML=`<b>🔔 Notifications</b>${items.length?items.map(n=>`<div class="notice"><b>${esc(n.type==="application"?n.candidate_name:"Application Update")}</b><div>${esc(n.message)}</div><small>${fmtDate(n.created_at)}</small></div>`).join(""):`<p style="color:#777">No notifications yet.</p>`}`;
  }catch(e){box.innerHTML="<b>🔔 Notifications</b><p>Unable to load notifications.</p>";}
}
function bell(){
  return `<button onclick="openNotifications()" style="border:0;background:transparent;cursor:pointer;font-size:18px">🔔 <b class="badge">!</b></button><div id="notifications" class="notice-panel hidden"></div>`;
}
/* =========================================
   CAREERCONNECT DARK / LIGHT MODE
========================================= */

(function () {

    const themeButton = document.querySelector(".icon-btn");

    // Load saved theme
    const savedTheme = localStorage.getItem("careerconnect-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");

        if (themeButton) {
            themeButton.textContent = "☀";
            themeButton.title = "Switch to Light Mode";
        }
    } else {
        if (themeButton) {
            themeButton.textContent = "◐";
            themeButton.title = "Switch to Dark Mode";
        }
    }

    // Theme button
    if (themeButton) {

        themeButton.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

            const isDark =
                document.body.classList.contains("dark-mode");

            if (isDark) {

                localStorage.setItem(
                    "careerconnect-theme",
                    "dark"
                );

                themeButton.textContent = "☀";
                themeButton.title = "Switch to Light Mode";

            } else {

                localStorage.setItem(
                    "careerconnect-theme",
                    "light"
                );

                themeButton.textContent = "◐";
                themeButton.title = "Switch to Dark Mode";
            }

        });

    }

})();