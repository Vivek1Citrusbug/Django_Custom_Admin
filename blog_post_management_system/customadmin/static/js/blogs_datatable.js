$(document).ready(function () {
    let table = $("#blogs.blogpost-table").DataTable({
      paging: true,
      responsive: true,
      pageLength: 10,
      autoWidth: false,
      lengthMenu: [10, 25, 50, 100],
      searching: true,
      processing: true,
      serverSide: true,
      ajax: {
        // context: this,
        url: window.datatable_url,
        type: "get",
      },
      columns: [
        { data: "id", name: "id", },
        { data: "title", name: "title" },
        { data: "content", name: "content" },
        { data: "date_published", name: "date_published" },
        { data: "author_id", name: "author_id" },
        { data: "action", name: "action" },
      ],
      // columnDefs: [{ orderable: false, targets: [1, 6] }],
      order: [[0, "asc"]],
      oLanguage: {
        sSearch: "",
        oPaginate: {
          sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
          sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
        },
      },
    });
  
    // table.on("click", "tbody tr", function () {
    //   location.href = `/customadmin/user/${table.row(this).data().id}`
    // });
    
  // };
  
  });
  