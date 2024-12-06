$(document).ready(function () {
  $("#standuptimer-table").DataTable({
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
      {
        render: function (data, type, JsonResultRow, meta) {
          return `<div class="abc" onclick="location.href='/admin/timers/${
            JsonResultRow._id
          }/update'">
                    <a class="link-dark w-100" href="/admin/timers/${
                      JsonResultRow._id
                    }/update">${Math.ceil(JsonResultRow.duration / 60)}</a>
              </div>`;
        },
        data: "duration",
        name: "duration",
      },
      { data: "recommended", name: "recommended" },
      { data: "created_at", name: "created_at" },
      { data: "action", name: "action" },
    ],
    order: [[1, "desc"]],
    columnDefs: [{ orderable: false, targets: [2] }],

    oLanguage: {
      sSearch: "",
      oPaginate: {
        sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
        sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
      },
    },
  });
});
