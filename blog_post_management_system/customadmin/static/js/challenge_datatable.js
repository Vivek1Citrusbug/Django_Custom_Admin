$(document).ready(function () {
  $("#challenge-table").DataTable({
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
          return `<div class="abc" onclick="location.href='/admin/challenge/${JsonResultRow._id}/update'">
                      <a class="link-dark w-100" href="/admin/challenge/${JsonResultRow._id}/update">${JsonResultRow.name}</a>
                </div>`;
        },
        data: "name",
        name: "name",
      },
      { data: "start_date", name: "start_date" },
      { data: "end_date", name: "end_date" },
      { data: "recommended", name: "recommended" },
      { data: "challenge_type", name: "challenge_type" },
      { data: "action", name: "action" },
    ],
    order: [[1, "desc"]],
    columnDefs: [{ orderable: false, targets: [5] }],

    oLanguage: {
      sSearch: "",
      oPaginate: {
        sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
        sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
      },
    },
  });
});
