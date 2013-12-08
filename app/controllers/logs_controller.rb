class LogsController < ApplicationController

  before_filter :authenticate_user!
	
  # GET /users/<id>/logs
  # GET /users/<id>/logs.json
  def index
    @logs = Log.where(user_id: params[:user_id])

    respond_to do |format|
      format.html
      format.json { render json: @logs }
    end
  end

  
  # GET /users/<id>/logs/<id>
  # GET /users/<id>/logs/<id>.json
  def show
    @log = Log.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: LogDatatable.new(view_context) }
    end
  end

  # GET /users/<id>/logs/new
  # GET /users/<id>/logs/new.json
  def new
    @log = Log.new
  end

  # POST /users/<id>/logs
  # POST /users/<id>/logs.json
  def create
    @log = Log.new(params[:log])
    @log.save
    respond_with @log
  end

  # DELETE /users/<id>/logs/<id>
  # DELETE /users/<id>/logs/<id>.json
  def destroy
    @log = Log.find(params[:id])
    @log.destroy

    respond_to do |format|
      format.html { redirect_to logs_url }
      format.json { head :ok }
    end
end

