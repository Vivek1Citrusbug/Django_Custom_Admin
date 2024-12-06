$(document).ready(function () {
  const currentDate = new Date();

  // Get the time zone using Intl.DateTimeFormat
  const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  $("#company-table").DataTable({
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
          <div onclick="location.href='/admin/company/${JsonResultRow._id}/dashboard/?timezone=${timeZone}'" style="display: flex;justify-content: start;gap: 0 15px;align-items: center;">
            <img width="50px" style="border-radius: 50%;object-fit: cover;"  height="50px" alt="company-logo" src="${JsonResultRow.logo}">
            <a  class="link-dark" href="/admin/company/${JsonResultRow._id}/dashboard/?timezone=${timeZone}">${JsonResultRow.name}</a>
          </div>`;
        },
        data: "name",
        name: "name",
      },
      {
        render: function (data, type, JsonResultRow, meta) {
          return `<td>${JsonResultRow.employees} / ${JsonResultRow.license}</td>`;
        },
        data: "employees",
        name: "employees",
      },
      { data: "created_at", name: "created_at" },
      { data: "action", name: "action" },
    ],
    order: [[2, "desc"]],
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
