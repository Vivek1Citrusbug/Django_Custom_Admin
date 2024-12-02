$(document).ready(function () {
  $("#nudging-table").DataTable({
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
              <div onclick="location.href='/admin/nudging/${JsonResultRow._id}/update'" style="display: flex;justify-content: start;gap: 0 15px;align-items: center;">
                <img width="50px" style="border-radius: 50%;object-fit: cover;"  height="50px" alt="company-logo" src="${JsonResultRow.picture}">
                <a  class="link-dark" href="/admin/nudging/${JsonResultRow._id}/update">${JsonResultRow.title}</a>
              </div>`;
        },
        data: "title",
        name: "title",
      },
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
