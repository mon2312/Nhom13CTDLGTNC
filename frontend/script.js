let allWords = [];

// Tải danh sách từ khi trang tải xong
window.onload = async function () {
    try {
        const response = await fetch("http://localhost:5000/all");
        allWords = Object.keys(await response.json());
    } catch (e) {
        console.error("Không thể tải từ điển:", e);
    }
}

async function searchWord() {
    const input = document.getElementById("searchInput");
    const resultDiv = document.getElementById("result");
    const suggestList = document.getElementById("suggestList");
    suggestList.innerHTML = ""; // Ẩn gợi ý khi tra cứu
    const word = input.value.trim();

    if (!word) {
        resultDiv.innerText = "⚠️ Vui lòng nhập từ cần tra.";
        return;
    }

    resultDiv.innerText = "Đang tra cứu...";

    const start = performance.now(); // ⏱️ Bắt đầu đo thời gian

    try {
        const response = await fetch(`http://localhost:5000/search?word=${encodeURIComponent(word)}`);
        const data = await response.json();

        const end = performance.now(); // ⏱️ Kết thúc đo thời gian
        const duration = (end - start).toFixed(2); // Tính thời gian ms

        if (response.ok) {
            resultDiv.innerHTML = `✅ <strong>${data.word}</strong>: ${data.meaning}<br>⏱️ Thời gian tra cứu: ${duration} ms`;
        } else {
            let message = `❌ ${data.error}`;
            if (data.suggestions && data.suggestions.length > 0) {
                message += `<br><em>🔎 Gợi ý:</em> ${data.suggestions.join(', ')}`;
            }
            message += `<br>⏱️ Thời gian tra cứu: ${duration} ms`;
            resultDiv.innerHTML = message;
        }
    } catch (error) {
        resultDiv.innerText = "🚫 Lỗi kết nối với server.";
    }
}


async function addWord() {
    const word = document.getElementById("newWord").value.trim();
    const meaning = document.getElementById("newMeaning").value.trim();
    const resultDiv = document.getElementById("result");

    if (!word || !meaning) {
        resultDiv.innerText = "⚠️ Vui lòng nhập đủ từ và nghĩa.";
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ word, meaning })
        });
        const data = await response.json();

        if (response.ok) {
            resultDiv.innerText = `✔️ ${data.message}`;
            allWords.push(word); // Cập nhật danh sách từ
        } else {
            resultDiv.innerText = `❌ ${data.error}`;
        }
    } catch (error) {
        resultDiv.innerText = "🚫 Lỗi khi thêm từ.";
    }
}

async function deleteWord() {
    const word = document.getElementById("deleteInput").value.trim();
    const resultDiv = document.getElementById("result");

    if (!word) {
        resultDiv.innerText = "⚠️ Vui lòng nhập từ cần xoá.";
        return;
    }

    try {
        const response = await fetch(`http://localhost:5000/delete?word=${encodeURIComponent(word)}`, {
            method: "DELETE"
        });
        const data = await response.json();

        if (response.ok) {
            resultDiv.innerText = `🗑️ ${data.message}`;
            allWords = allWords.filter(w => w !== word); // Xoá khỏi gợi ý
        } else {
            resultDiv.innerText = `❌ ${data.error}`;
        }
    } catch (error) {
        resultDiv.innerText = "🚫 Lỗi khi xoá từ.";
    }
}

function showSuggestions() {
    const input = document.getElementById("searchInput");
    const suggestList = document.getElementById("suggestList");
    const text = input.value.trim().toLowerCase();
    suggestList.innerHTML = "";

    if (!text) return;

    const matches = allWords.filter(word => word.startsWith(text)).slice(0, 5);
    matches.forEach(word => {
        const li = document.createElement("li");
        li.textContent = word;
        li.onclick = () => {
            input.value = word;
            suggestList.innerHTML = "";
            searchWord();
        };
        suggestList.appendChild(li);
    });
}
