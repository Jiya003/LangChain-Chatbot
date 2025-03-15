function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    if (userInput.trim() === "") return;

    // Add user message to chat
    chatBox.innerHTML += `<div class="user-msg">You: ${userInput}</div>`;

    // Send request to Flask API
    fetch(`/search?query=${encodeURIComponent(userInput)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                chatBox.innerHTML += `<div class="bot-msg">Bot: ${data.error}</div>`;
            } else if (data.results.length > 0) {
                let responseText = "<strong>Recommended Courses:</strong><br>";
                data.results.forEach(course => {
                    let description=course.detailed_description? course.detailed_description:"N/A"
                    let courseLink = course.course_link ? course.course_link : "#";
                    let pricePerSession = course.price_per_session ? course.price_per_session : "N/A";
                    let numLessons = course.number_of_lessons ? course.number_of_lessons : "N/A";
                    let totalPrice = course.total_price ? course.total_price : "N/A";

                    responseText += `
                        <div class="course">
                            <strong>${course.title}</strong><br>
                            ${description}<br>
                            <strong>Price per session:</strong> ${pricePerSession}<br>
                            <strong>Number of lessons:</strong> ${numLessons}<br>
                            <strong>Total Price:</strong> ${totalPrice}<br>
                            <a href="${courseLink}" target="_blank">View Course</a><br><br>
                        </div>`;
                });
                chatBox.innerHTML += `<div class="bot-msg">${responseText}</div>`;
            } else {
                chatBox.innerHTML += `<div class="bot-msg">Bot: No relevant courses found.</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight; 
        })
        .catch(error => {
            chatBox.innerHTML += `<div class="bot-msg">Bot: Error fetching results.</div>`;
        });

    // Clear input field
    document.getElementById("user-input").value = "";
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
