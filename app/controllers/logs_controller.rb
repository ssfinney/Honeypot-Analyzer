class LogsController < ApplicationController

  before_filter :authenticate_user!
	
  def index
    respond_to do |format|
      format.html
      format.json { render json: LogDatatable.new(view_context) }
    @logs = Log.all
  end

  def new
    @log = Log.new
  end

  def create
    @log = Log.new(params[:log])
    @log.save
    respond_with @log
  end

  def show
    @log = Log.find(params[:id])
  end

end

