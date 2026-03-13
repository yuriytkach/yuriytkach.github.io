async function loadPosts() {
  const container = document.getElementById('posts');
  if (!container) return;
  const response = await fetch('/data/volunteer-posts.json');
  const posts = await response.json();
  container.innerHTML = posts.map((post) => `
    <a class="post-card" href="/volunteer/posts/${post.slug}/">
      ${post.cover ? `<img src="${post.cover}" alt="${post.title.replace(/"/g, '&quot;')}">` : ''}
      <div class="meta">
        <time datetime="${post.dateISO}">${post.dateHuman}</time>
        <h3>${post.title}</h3>
        <p>${post.excerpt}</p>
      </div>
    </a>
  `).join('');
}
loadPosts().catch((err) => console.error(err));
