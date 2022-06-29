function deleteUser(userId, csrf) {
fetch('/admin/deleteUser', {
    method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf
        },
    body: JSON.stringify({ userId: userId })
}).then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        window.location.href = data
    })
}

function deletePost(postId, csrf) {
fetch('/admin/deletePost', {
    method: 'POST',
    headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf
        },
    body: JSON.stringify({ postId: postId })
}).then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        window.location.href = data['url']
    })
}
