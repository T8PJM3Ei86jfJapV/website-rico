$('#pagination-demo').twbsPagination({
  totalPages: parseInt($('#total-pages').text()),
  visiblePages: 7,
  first: '首页',
  prev: '上一页',
  next: '下一页',
  last: '尾页',
  href: '?page={{number}}',
});
