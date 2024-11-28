$(document).ready(function () {
  let table = $("#user-table").DataTable({
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
          return `<div onclick="location.href='/admin/user/${
            JsonResultRow._id
          }/update'"><a class="link-dark" href="/admin/user/${
            JsonResultRow._id
          }/update">${
            !!!(JsonResultRow.first_name + JsonResultRow.last_name)
              ? "-"
              : JsonResultRow.first_name + " " + JsonResultRow.last_name
          }</a></div>`;
        },
        data: "first_name",
        name: "first_name",
      },
      // {
      //   render: function (data, type, JsonResultRow, meta) {
      //     return `<div onclick="location.href='/admin/company/${
      //       JsonResultRow.company_id
      //     }/update'"><a class="link-dark" href="/admin/company/${
      //       JsonResultRow.company_id
      //     }/update">${
      //       !!!JsonResultRow.company ? "-" : JsonResultRow.company
      //     }</a></div>`;
      //   },
      // },
      { data: "email", name: "email" },
      { data: "created_at", name: "created_at" },
      { data: "user_type", name: "user_type" },
      { data: "is_active", name: "is_active" },
      { data: "action", name: "action" },
    ],
    columnDefs: [{ orderable: false, targets: [1, 6] }],
    order: [[3, "desc"]],
    oLanguage: {
      sSearch: "",
      oPaginate: {
        sNext: `<a href="#" aria-controls="user-table" data-dt-idx="4" tabindex="0" class="page-link">></a>`,
        sPrevious: `<a href="#" aria-controls="user-table" data-dt-idx="0" tabindex="0" class="page-link"><</a>`,
      },
    },
  });
  // table.on("click", "tbody tr", function () {
  //   location.href = `/admin/user/${table.row(this).data()._id}/update`;
  // });
});
