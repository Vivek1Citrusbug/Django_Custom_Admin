$(document).ready(function () {
    let table = $("#blogpost-table").DataTable({
      paging: true,
      responsive: true,
      pageLength: 10,
      autoWidth: false,
      lengthMenu: [10, 25, 50, 100],
      searching: true,
      processing: true,
      serverSide: true,
      ajax: {
        url: window.datatable_url,
        type: "get",
      },
      columns: [
        { data: "id", name: "id", orderable:true },
        { data: "title", name: "title", orderable:true },
        { data: "content", name: "content", orderable:true },
        { data: "date_published", name: "date_published", orderable:true },
        { data: "author_id", name: "author_id", orderable:true },
        { data: "action", name: "action", orderable:true },
      ],
      columnDefs: [{ orderable: true, targets: [0,1] }],
      order: [[3, "desc"]],
      oLanguage: {
        sSearch: "",
        oPaginate: {
          sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
          sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
        },
      },
      
    });

    table.columns([0, 2]).visible(false);
    table.order([3, 'desc']).draw();
   

    table.on("click", "tbody tr", function () {
    location.href = `/customadmin/posts/${table.row(this).data().id}`
  });
    
  // };
  
  });
  
