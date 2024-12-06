$(document).ready(function () {
  $("#event-table").DataTable({
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
          return `
            <div onclick="location.href='/admin/events/${JsonResultRow._id}/update" style="display: flex;justify-content: start;gap: 0 15px;align-items: center;">
              <a  class="link-dark" href="/admin/events/${JsonResultRow._id}/update">${JsonResultRow.name}</a>
            </div>`;
        },
        data: "name",
        name: "name",
      },
      {
        data: "starts_at",
        name: "starts_at",
      },
      { data: "ends_at", name: "ends_at" },
      { data: "action", name: "action" },
    ],
    order: [[1, "asc"]],
    columnDefs: [{ orderable: false, targets: [3] }],

    oLanguage: {
      sSearch: "",
      oPaginate: {
        sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
        sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
      },
    },
  });
});
