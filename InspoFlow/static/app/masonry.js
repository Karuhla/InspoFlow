function applyMasonryLayout() {
    const grid = document.querySelector('.image-grid');
    const items = Array.from(grid.children);
  
    // Determine column count based on available grid width and item width (350px)
    const columnCount = Math.max(1, Math.floor(grid.offsetWidth / 350)); 
    const columnWidths = Array(columnCount).fill(0);
  
    // Reset grid layout (avoid conflicting positioning with CSS)
    grid.style.position = 'relative';
  
    // Position items in the shortest column
    items.forEach(item => {
      item.style.position = 'absolute';
      const shortestColumnIndex = columnWidths.indexOf(Math.min(...columnWidths));
      const topPosition = columnWidths[shortestColumnIndex];
      const leftPosition = shortestColumnIndex * (grid.offsetWidth / columnCount); // Dynamically calculate column width
  
      item.style.top = `${topPosition}px`;
      item.style.left = `${leftPosition}px`;
  
      columnWidths[shortestColumnIndex] += item.offsetHeight + 10; // Add spacing
    });
  
    // Set the grid height to fit all items
    grid.style.height = `${Math.max(...columnWidths)}px`;
  
    // Adjust grid width to ensure content is centered
    const totalWidth = grid.offsetWidth;
    const windowWidth = window.innerWidth;
    const marginLeft = (windowWidth - totalWidth) / 2 + 10;
    grid.style.marginLeft = `${marginLeft}px`;
}
  
// Reapply masonry layout on window resize or load
window.addEventListener('load', applyMasonryLayout);
window.addEventListener('resize', applyMasonryLayout);
