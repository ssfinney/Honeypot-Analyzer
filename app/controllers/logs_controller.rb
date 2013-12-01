class LogsController < ApplicationController
	
  def index
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

