document.addEventListener('DOMContentLoaded', () => {
    const posts = document.querySelectorAll('.post');

    posts.forEach(post => {
        const post_id = post.getAttribute('data-post-id');
        const post_content = post.querySelector('.post_content');
        const edit_button = post.querySelector('.edit_button');
        const edit_textarea = post.querySelector('.edit_textarea');
        const save_button = post.querySelector('.save_button');
        const cancel_button = post.querySelector('.cancel_button');
        const like_button = post.querySelector('.like_button');

        like_button.addEventListener('click', () => {
            fetch(`/like/post_id=${post_id}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const new_likes = data['likes'];
                like_button.innerHTML = `<i class="fas fa-heart"></i> Likes (${new_likes})`;
                if (data['like']){
                    like_button.style.color = 'red';
                }
                else if (data['unlike']){
                    like_button.style.color = 'aliceblue';
                    // hover effect not working without this extra style change, it's value could be anything
                    // also how to set hover property in js
                    like_button.style = '';
                }
                
                
            });
        });

        if (edit_button) {
            edit_button.addEventListener('click', () => {
                post_content.style.display = 'none';
                edit_textarea.style.display = 'block';
                edit_button.style.display = 'none';
                save_button.style.display = 'block';
                cancel_button.style.display = 'block';
            }); 
        }

        if (save_button) {
            save_button.addEventListener('click', () => {
                post_content.textContent = edit_textarea.value;
                post_content.style.display = 'block';
                edit_textarea.style.display = 'none';
                edit_button.style.display = 'block';
                save_button.style.display = 'none';
                cancel_button.style.display = 'none';
    
                // send new post_content to backend
                const new_content = post_content.textContent;
                const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
                fetch(`/post/id=${post_id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf_token },
                    body: JSON.stringify({
                        content: new_content
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                });
            });
        }

        if (cancel_button) {
            cancel_button.addEventListener('click', () => {
                post_content.style.display = 'block';
                edit_textarea.value = post_content.textContent;
                edit_textarea.style.display = 'none';
                edit_button.style.display = 'block';
                save_button.style.display = 'none';
                cancel_button.style.display = 'none';
    
                console.log(`post: ${post_id} edit cancelled`);
            });  
        }
    });
});