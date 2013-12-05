# TODO: Expand full text search to Sphinx or Solar if necessary.
# TODO: Add a log_id parameter to pass here in order to display only entries for this log.
# TODO: Maybe downgrade to Rails 3?
# Class modified from <NAME> as seen on RailsCast #340: DataTables.
# It defines a custom class to serve data from rails to the datatable as it's needed.

class LogDatatable
  delegate :params, :h, :link_to, to: :@view

  def initialize(view)
    @view = view
  end

  def as_json(options = {})
    {
      sEcho: params[:sEcho].to_i,
      iTotalRecords: Entry.where(id: params[:log_id]).count,
      iTotalDisplayRecords: entries.total_entries,
      aaData: data
    }
  end

private

  def data
    entries.map do |entry|
      [
        h(entry.id),
	h(entry.date),
	h(entry.time),
	h(entry.protocol),
	h(entry.conn_type),
	h(entry.src_port),
	h(entry.dest_port),
	h(entry.src_ip),
	h(entry.dest_ip),
	h(entry.info),
	h(entry.environment)
      ]
    end
  end

  def entries
    @entries ||= fetch_entries
  end

  def fetch_entries
    entries = Entry.where(id: params[:log_id]).order("#{sort_column} #{sort_direction}")
    entries = entries.page(page).per_page(per_page)
    if params[:sSearch].present?
      entries = entries.where("name like :search or category like :search", search: "%#{params[:sSearch]}%")
    end
    entries
  end

  def page
    params[:iDisplayStart].to_i/per_page + 1
  end

  def per_page
    params[:iDisplayLength].to_i > 0 ? params[:iDisplayLength].to_i : 10
  end

  def sort_column
    columns = %w[name category released_on price]
    columns[params[:iSortCol_0].to_i]
  end

  def sort_direction
    params[:sSortDir_0] == "desc" ? "desc" : "asc"
  end

end

