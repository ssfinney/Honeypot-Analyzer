# This file defines how the DataTable for the Log view should operate

jQuery -> 
  $('#log').dataTable
  sPaginationType: "full_numbers"	# Use full number pagination
  bProcessing: true 			# Shows a "processing" message while fetching data
  bServerSide: true			# Sets fetching data from server-side
  sAjaxSource: $('#log').data('source')	# Supplies source URL to fetch data from

