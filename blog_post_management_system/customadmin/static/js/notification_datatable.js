$(document).ready(function () {
  $("#notification-table").DataTable({
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
      { data: "user", name: "user" },
      {
        data: "title",
        name: "title",
      },

      { data: "notification_type", name: "notification_type" },
      { data: "read", name: "read" },
      { data: "created_at", name: "created_at" },
    ],
    order: [[4, "desc"]],

    oLanguage: {
      sSearch: "",
      oPaginate: {
        sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
        sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
      },
    },
  });
});
