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
      { data: "id",name:"id"},
      { data: "username",name: "username"},
      { data: "first_name",name: "first_name"},
      { data: "last_name",name: "first_name"},
      { data: "email", name: "email" },
      { data: "date_joined", name: "date_joined" },
      { data: "is_active", name: "is_active" },
      { data: "is_staff", name: "is_staff" },
      { data: "last_login", name: "last_login" },
      {
        render: function (data, type, JsonResultRow, meta) {
          return `<div onclick="location.href='/customadmin/user/${JsonResultRow.id}/update'"><a class="link-dark" href="/customadmin/user/${JsonResultRow.id}/update">Update</a></div>`},
        data: "first_name",
        name: "first_name",
      },
      
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
