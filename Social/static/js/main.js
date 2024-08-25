function toggleCommentModal(postId) {
  var modal = document.getElementById('commentModal' + postId);
  if (modal.style.display === "block") {
      modal.style.display = "none";
  } else {
      modal.style.display = "block";
  }
}

function closeCommentModal(postId) {
  var modal = document.getElementById('commentModal' + postId);
  modal.style.display = "none";
}