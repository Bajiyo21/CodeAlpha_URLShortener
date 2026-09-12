// Copy Button

document.querySelectorAll(".copy-btn").forEach(button=>{

    button.addEventListener("click",()=>{

        navigator.clipboard.writeText(button.dataset.link);

        button.innerHTML="✅ Copied";

        setTimeout(()=>{
            button.innerHTML="📋 Copy";
        },1500);

    });

});

// Search Filter

const searchInput=document.getElementById("searchInput");
const rows=document.querySelectorAll("#historyTable tbody tr");

searchInput.addEventListener("keyup",()=>{

    const value=searchInput.value.toLowerCase();

    rows.forEach(row=>{

        row.style.display=
            row.innerText.toLowerCase().includes(value)
            ?""
            :"none";

    });

});